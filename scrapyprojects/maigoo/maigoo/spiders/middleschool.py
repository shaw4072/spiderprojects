# -*- coding: utf-8 -*-
from datetime import datetime

import scrapy
from scrapy_splash import SplashRequest

# js脚本：点击加载更多
# '''document.onreadystatechange = subSomething;'''
from maigoo.items import MongoItem

load_more_js='''
    function subSomething() {
        var eles = document.querySelectorAll('a.addmore3.bgcolor')
        for (var i=0;i<eles.length;i++){
            var v = eles[i];
            while (v.className.indexOf('snomore') == -1){
                v.click();
            }
        }
    };
  	subSomething();
'''

# lua脚本：渲染js
lua_source='''
function main(splash, args)
      assert(splash:wait(0.5))

      splash:set_custom_headers({
        ['Accept'] = '*/*',
        ['Accept-Language'] = 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        ['Cache-Control'] = 'max-age=0',
        ['Connection'] = 'keep-alive',
        ['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
      })
  		local load_more_js =[[
  			function subSomething() {
            var eles = document.querySelectorAll('a.addmore3.bgcolor')
            for (var i=0;i<eles.length;i++){
  							var v = eles[i];
                while (v.className.indexOf('snomore') == -1){
                    		v.click();
                		}
            		}
    		};
  		    subSomething();
        ]]
      
      splash.private_mode_enabled = false
      assert(splash:go(args.url))
      assert(splash:wait(3))
  		
  		assert(splash:runjs(load_more_js))

      return {
        html = splash:html()
      }
end
'''

class MiddleschoolSpider(scrapy.Spider):
    name = 'middleschool'
    allowed_domains = ['www.maigoo.com']
    start_urls = ['https://www.maigoo.com/news/487820.html']

    custom_settings = {
        # "MONGO_COLLECTION": "middleschool_test",
        "MONGO_COLLECTION": "middleschool",
    }

    def parse(self, response):
        pro_eles=response.xpath('//*[@id="t_container"]/div[position()>7]/div/div[@class="mod_cont"]/div/ul/li/a')
        for pro_ele in pro_eles:
            nexturl = pro_ele.xpath("./@href").extract_first()
            provincename = pro_ele.xpath(".//span/text()").extract_first()
            # if "江苏" not in provincename:continue
            datanode={
                'provincename':provincename,
            }
            sourcenode={
                'source':response.urljoin(response.url),
                'crawltime':datetime.now()
            }
            node={
                'datanode':datanode,
                'sourcenode':sourcenode
            }
            print(f"provincename:{provincename}\ nexturl:{nexturl}")
            yield SplashRequest(
                nexturl,
                meta={'node':node},
                endpoint='execute',
                args={'lua_source':lua_source},
                cache_args=['lua_source'],
                callback=self.parseurl1
                )

    def parseurl1(self,response):
        mitem=MongoItem()
        # with open("tmp.html","wb") as f:
        #     f.write(response.body)
        penode = response.meta['node']

        boolean_ele=response.xpath("//div[@id='t_container']/div[4]/div/div/div[contains(@class,'gobtn')]/span//text()")
        boolean_ele_text=boolean_ele.extract_first()
        # print(f"boolean_ele_text:{boolean_ele_text}")
        n=4 if boolean_ele_text is not None else 3

        div_eles = response.xpath(f"//div[@id='t_container']/div[position()>{n} and position() < last()-2][position() mod 2 = 1]")

        sourcenode = {
            'source': response.urljoin(response.url),
            'crawltime': datetime.now()
        }
        node = {
            'sourcenode': sourcenode,
        }

        for div_ele in div_eles:
            div_next_ele = div_ele.xpath("./following-sibling::div[1]")
            citysite = div_ele.xpath(".//div[contains(@class,'mod_title')]//text()").extract()
            citysite=''.join(citysite).strip()
            tr_eles=div_next_ele.xpath(".//tr[td]")

            for tr_ele in tr_eles:
                schoolname=tr_ele.xpath("./td[2]//text()").extract_first()
                schoolurl=tr_ele.xpath("./td[2]/a/@href").extract_first()
                schoolsite=tr_ele.xpath("./td[3]//text()").extract_first()
                datanode={
                    'citysite':citysite,
                    'schoolname':schoolname,
                    'schoolurl':schoolurl,
                    'schoolsite':schoolsite
                }
                node['datanode']=datanode
                penode['node']=node
                mitem['node']=penode
                yield mitem
        # print(f"node:{node}")
