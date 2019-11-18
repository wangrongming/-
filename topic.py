@tenacity.retry(stop=stop_after_attempt(3), after=get_proxy, wait=wait_fixed(0.1))
def __h5api_producer(self, pro, fw):
    time.sleep(0.2)
    final_url = self.__h5api_url.format(pro['spu'])
    res = requests.get(url=final_url, headers=self.__search_headers, timeout=5)
    if "redirecturl" in res.text:
        return
    html = res.json()
    try:
        # print(html)
        data = html.get("data")
        title = data['item']['title']
        sku_base = data['skuBase']
        props = data['props']

        brand = ""
        model = ""
        try:
            brand_info = props['groupProps'][0]["基本信息"][0]
            if "品牌" in brand_info.keys():
                brand = brand_info[list(brand_info.keys())[0]]
            base_info = props['groupProps'][0]["基本信息"]
            for model_info in base_info:
                if "型号" in list(model_info.keys())[0]:
                    model = model_info[list(model_info.keys())[0]]
                    break
        except:
            print(traceback.format_exc())
            pass

        skus_li = sku_base.get('skus')
        if not skus_li:
            item = {
                "spu": pro['spu'],
                "title": title,
                "shop_name": pro['shop_name'],
                "search_brand": pro['search_brand'],
                "search_model": pro['search_model'],
                "real_brand": brand,
                "real_model": model,
                "sku": "",
                "color": "",
            }
            fw.write(json.dumps(item, ensure_ascii=False))
            fw.write("\n")
            print(item)
            self.collection.insert_one(item)
            return

        for skus in skus_li:
            sku_id = skus['skuId']
            item = {
                "spu": pro['spu'],
                "title": title,
                "shop_name": pro['shop_name'],
                "search_brand": pro['search_brand'],
                "search_model": pro['search_model'],
                "real_brand": brand,
                "real_model": model,
                "sku": sku_id,
                "color": color,
            }
            fw.write(json.dumps(item, ensure_ascii=False))
            fw.write("\n")
            self.collection.insert_one(item)  # 存储数据库
            print(item)

    except Exception as e:
        print(pro['spu'], traceback.format_exc())
        self.logger.error(e)
