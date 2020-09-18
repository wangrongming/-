# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @Time : 2020/9/18 9:19
 @IDE  : PyCharm
 """
import json

import pandas as pd
from pymongo import MongoClient

final_res = {'576752333004': {'北京': '3009', '上海': '3009', '广州': '3009', '成都': '3009', '武汉': '3009'},
             '520854626114': {'北京': '151', '上海': '151', '广州': '151', '成都': '151', '武汉': '151'},
             '597906281044': {'北京': '121', '上海': '121', '广州': '121', '成都': '121', '武汉': '121'},
             '45851160786': {'北京': '718', '上海': '718', '广州': '718', '成都': '718', '武汉': '718'},
             '573050347697': {'北京': '454', '上海': '454', '广州': '454', '成都': '454', '武汉': '454'},
             '582712074931': {'北京': '1328', '上海': '1328', '广州': '1328', '成都': '1328', '武汉': '1328'},
             '528134348419': {'北京': '446', '上海': '446', '广州': '446', '成都': '446', '武汉': '446'},
             '7853942925': {'北京': '2907', '上海': '2907', '广州': '2907', '成都': '2907', '武汉': '2907'},
             '525566678785': {'北京': '330', '上海': '330', '广州': '330', '成都': '330', '武汉': '330'},
             '520953103416': {'北京': '1567', '上海': '1567', '广州': '1567', '成都': '1567', '武汉': '1567'},
             '523253365162': {'北京': '1785', '上海': '1785', '广州': '1785', '成都': '1785', '武汉': '1785'},
             '526586148621': {'北京': '9160', '上海': '9160', '广州': '9160', '成都': '9160', '武汉': '9160'},
             '38889879566': {'北京': '2894', '上海': '2894', '广州': '2894', '成都': '2894', '武汉': '2894'},
             '611982246419': {'北京': '5029', '上海': '5029', '广州': '5029', '成都': '5029', '武汉': '5029'},
             '574792175595': {'北京': '11007', '上海': '11007', '广州': '11007', '成都': '11007', '武汉': '11007'},
             '15134720922': {'北京': '26864', '上海': '26864', '广州': '26864', '成都': '26864', '武汉': '26864'},
             '601510748822': {'北京': '7315', '上海': '7315', '广州': '7315', '成都': '7315', '武汉': '7315'},
             '13620302567': {'北京': '36558', '上海': '36558', '广州': '36558', '成都': '36558', '武汉': '36558'},
             '575462877812': {'北京': '13', '上海': '13', '广州': '13', '成都': '4', '武汉': '6'},
             '609088483259': {'北京': '179', '上海': '179', '广州': '179', '成都': '179', '武汉': '179'},
             '571158274871': {'北京': '12', '上海': '16', '广州': '14', '成都': '12', '武汉': '13'},
             '14758724899': {'北京': '15', '上海': '47', '广州': '44', '成都': '42', '武汉': '65'},
             '595303051756': {'北京': '5', '上海': '7', '广州': '5', '成都': '10', '武汉': '11'},
             '575855849231': {'北京': '9', '上海': '65', '广州': '28', '成都': '15', '武汉': '33'},
             '582691708627': {'北京': '8', '上海': '13', '广州': '8', '成都': '9', '武汉': '11'},
             '574948341557': {'北京': '143', '上海': '143', '广州': '143', '成都': '143', '武汉': '143'},
             '613771658186': {'北京': '13', '上海': '17', '广州': '12', '成都': '12', '武汉': '15'},
             '596189802969': {'北京': '50', '上海': '44', '广州': '46', '成都': '41', '武汉': '85'},
             '17526450484': {'北京': '25', '上海': '23', '广州': '102', '成都': '55', '武汉': '98'},
             '572070567283': {'北京': '3112', '上海': '3112', '广州': '3112', '成都': '3112', '武汉': '3112'},
             '567500254275': {'北京': '3949', '上海': '3949', '广州': '3949', '成都': '3949', '武汉': '3949'},
             '596032735271': {'北京': '1682', '上海': '1682', '广州': '1682', '成都': '1682', '武汉': '1682'},
             '598739041836': {'北京': '6354', '上海': '6354', '广州': '6354', '成都': '6354', '武汉': '6354'},
             '530276433158': {'北京': '157', '上海': '157', '广州': '157', '成都': '157', '武汉': '157'},
             '17430326435': {'北京': '136', '上海': '136', '广州': '136', '成都': '136', '武汉': '136'},
             '526556018131': {'北京': '435', '上海': '435', '广州': '435', '成都': '435', '武汉': '435'},
             '578241474911': {'北京': '399', '上海': '399', '广州': '399', '成都': '399', '武汉': '399'},
             '537140825702': {'北京': '8369', '上海': '8369', '广州': '8369', '成都': '8369', '武汉': '8369'},
             '534502397490': {'北京': '5773', '上海': '5773', '广州': '5773', '成都': '5773', '武汉': '5773'},
             '602069617532': {'北京': '354', '上海': '354', '广州': '354', '成都': '354', '武汉': '354'},
             '525006412797': {'北京': '1352', '上海': '1352', '广州': '1352', '成都': '1352', '武汉': '1352'},
             '531492926930': {'北京': '530', '上海': '530', '广州': '530', '成都': '530', '武汉': '530'},
             '589279649038': {'北京': '1356', '上海': '1356', '广州': '1356', '成都': '1356', '武汉': '1356'},
             '601198422101': {'北京': '990', '上海': '990', '广州': '990', '成都': '990', '武汉': '990'},
             '620290229137': {'北京': '39987', '上海': '39987', '广州': '39987', '成都': '39987', '武汉': '39987'},
             '527079137591': {'北京': '10235', '上海': '10235', '广州': '10235', '成都': '10235', '武汉': '10235'},
             '527663550200': {'北京': '439', '上海': '439', '广州': '439', '成都': '439', '武汉': '439'},
             '19701119549': {'北京': '4', '上海': '10', '广州': '22', '成都': '10', '武汉': '10'},
             '553262031222': {'北京': '21', '上海': '33', '广州': '39', '成都': '30', '武汉': '41'},
             '612358544672': {'北京': '74', '上海': '74', '广州': '74', '成都': '74', '武汉': '74'},
             '585113390663': {'北京': '79', '上海': '96', '广州': '86', '成都': '86', '武汉': '97'},
             '593584575302': {'北京': '374', '上海': '374', '广州': '374', '成都': '374', '武汉': '374'},
             '592200427884': {'北京': '8', '上海': '4', '广州': '6', '成都': '9', '武汉': '5'},
             '619319158015': {'北京': '6', '上海': '7', '广州': '11', '成都': '10', '武汉': '8'},
             '39449400718': {'北京': '400', '上海': '400', '广州': '400', '成都': '400', '武汉': '400'},
             '17745318960': {'北京': '10', '上海': '15', '广州': '22', '成都': '5', '武汉': '27'},
             '535912172004': {'北京': '774', '上海': '774', '广州': '774', '成都': '774', '武汉': '774'},
             '603190755436': {'北京': '8', '上海': '5', '广州': '10', '成都': '5', '武汉': '6'},
             '565940769356': {'北京': '8', '上海': '9', '广州': '2', '成都': '3', '武汉': '5'},
             '43822706889': {'北京': '12', '上海': '33', '广州': '7', '成都': '13', '武汉': '11'},
             '612869424149': {'北京': '10000', '上海': '10000', '广州': '10000', '成都': '10000', '武汉': '10000'},
             '569655719387': {'北京': '639', '上海': '639', '广州': '639', '成都': '639', '武汉': '639'},
             '596508085415': {'北京': '10352', '上海': '10352', '广州': '10352', '成都': '10352', '武汉': '10352'},
             '588281024971': {'北京': '35681', '上海': '35681', '广州': '35681', '成都': '35681', '武汉': '35681'},
             '560314484665': {'北京': '25', '上海': '25', '广州': '32', '成都': '30', '武汉': '21'},
             '601084823311': {'北京': '11', '上海': '36', '广州': '29', '成都': '14', '武汉': '14'},
             '558490066078': {'北京': '474', '上海': '474', '广州': '474', '成都': '474', '武汉': '474'},
             '583273797163': {'北京': '2527', '上海': '4898', '广州': '2475', '成都': '2227', '武汉': '1811'},
             '14061404967': {'北京': '2', '上海': '38', '广州': '42', '成都': '13', '武汉': '4'},
             '612515873452': {'北京': '33', '上海': '54', '广州': '159', '成都': '100', '武汉': '95'},
             '571300993084': {'北京': '503', '上海': '435', '广州': '977', '成都': '348', '武汉': '416'},
             '612756322851': {'北京': '294', '上海': '666', '广州': '291', '成都': '234', '武汉': '105'},
             '523245470255': {'北京': '2659', '上海': '6040', '广州': '3045', '成都': '2735', '武汉': '2561'},
             '526924651900': {'北京': '559', '上海': '2254', '广州': '1534', '成都': '647', '武汉': '1175'},
             '593645217773': {'北京': '184', '上海': '184', '广州': '48', '成都': '114', '武汉': '26'},
             '45517937143': {'北京': '1836', '上海': '5393', '广州': '7242', '成都': '1420', '武汉': '1815'},
             '543442473995': {'北京': '5264', '上海': '2611', '广州': '782', '成都': '10373', '武汉': '2375'}}

mongo = MongoClient("mongodb://192.168.140.231:28018/eqs_sales")
dest_db = mongo.get_database()

# tmall
tmall_goods_detail = dest_db.get_collection("tmall_goods_detail")
tmall_goods_config = dest_db.get_collection("tmall_goods_config")
tmall_goods_price = dest_db.get_collection("tmall_goods_price")
tmall_goods_promotion = dest_db.get_collection("tmall_goods_promotion")
tmall_goods_prom = dest_db.get_collection("tmall_goods_prom")
tmall_goods_stock = dest_db.get_collection("tmall_goods_stock")
# jd
jd_goods_detail = dest_db.get_collection("jd_goods_detail")
jd_goods_price = dest_db.get_collection("jd_price_20200918")
jd_goods_promotion = dest_db.get_collection("jd_goods_promotion")
jd_goods_prom = dest_db.get_collection("jd_goods_prom")

choashi = ['583273797163', '14061404967', '612515873452', '571300993084', '612756322851', '523245470255',
           '526924651900', '593645217773', '45517937143', '543442473995']


def export_tmall():
    dis_li = []
    detail_li = tmall_goods_detail.find({"data.status": {"$exists": True}})
    res_li = []
    for detail in detail_li:
        spu = detail["spu"]
        shop_name = detail.get("data", {}).get("seller", {}).get("shop_name", "")
        product_name = detail.get("data", {}).get("item", {}).get("title", "")
        status = detail.get("data", {}).get("status", "")
        spu_stock = detail.get("data", {}).get("spu_stock", "")
        spu_price = detail.get("data", {}).get("spu_price", "")
        # product_params = config['path_str']
        if spu in dis_li:
            continue
        dis_li.append(spu)

        # promotion
        promotion_li = tmall_goods_promotion.find({"spu": spu}).sort([("_id", -1)])
        promotion_dis = []
        if promotion_li.count() == 0:
            promotion = ""
        else:
            promotion_res = []
            for promotion in promotion_li:
                uuid = promotion.get("data", {}).get("uuid", "")
                if uuid in promotion_dis:
                    continue
                promotion_dis.append(uuid)
                subtitles = promotion.get("data", {}).get("subtitles", "")
                title = promotion.get("data", {}).get("title", "")
                coupon_name = promotion.get("data", {}).get("couponDisplayName", "")
                promotion_one = f"{subtitles}|{title}|{coupon_name}"
                promotion_res.append(promotion_one)
            promotion = json.dumps(promotion_res, ensure_ascii=False)

        # prom
        prom_li = tmall_goods_prom.find({"spu": spu}).sort([("_id", -1)])
        prom_dis = []
        if prom_li.count() == 0:
            prom_activity = ""
        else:
            prom_activity_li = []
            for prom in prom_li:
                activity_id = prom.get("data", {}).get("activityId", "")
                if activity_id in prom_dis:
                    continue
                prom_dis.append(activity_id)

                icon_text = prom.get("data", {}).get("iconText", "")
                title = prom.get("data", {}).get("title", "")
                type_ = prom.get("data", {}).get("type", "")
                contentText = prom.get("data", {}).get("contentText", "")
                prom_activity_one = f"{icon_text}|{title}|{type_}|{contentText}"
                prom_activity_li.append(prom_activity_one)
            prom_activity = json.dumps(prom_activity_li, ensure_ascii=False)

        # config
        dis_sku_li = []
        config_li = tmall_goods_config.find({"spu": spu})
        if config_li.count() > 0:
            for config in config_li:
                product_params = config['path_str']
                sku = config['sku']
                if sku in dis_sku_li:
                    continue
                dis_sku_li.append(sku)

                # price
                price = tmall_goods_price.find_one({"sku": sku})
                if price:
                    prom_price = price.get("price", "")
                else:
                    prom_price = ""

                # stock
                stock = tmall_goods_stock.find_one({"sku": sku})
                if stock:
                    stock_ = stock.get("quantity", "")
                else:
                    stock_ = ""

                # area
                if spu in choashi:
                    area = final_res.get(spu, "")
                    for key in area.keys():
                        item = {
                            "url": f"https://detail.tmall.com/item.htm?id={spu}&skuId={sku}",
                            "sku": sku,
                            "spu": spu,
                            "shop_name": shop_name,
                            "product_name": product_name,
                            "product_params": product_params,
                            "original_price": "",
                            "prom_price": prom_price,
                            "promotion": promotion,
                            "prom_activity": prom_activity,
                            "stock": stock_,
                            "status": status,
                            "area": f"{key}|{area[key]}",
                        }
                        res_li.append(item)
                else:
                    item = {
                        "url": f"https://detail.tmall.com/item.htm?id={spu}&skuId={sku}",
                        "sku": sku,
                        "spu": spu,
                        "shop_name": shop_name,
                        "product_name": product_name,
                        "product_params": product_params,
                        "original_price": "",
                        "prom_price": prom_price,
                        "promotion": promotion,
                        "prom_activity": prom_activity,
                        "stock": stock_,
                        "status": status,
                        "area": "",
                    }
                    res_li.append(item)
        else:
            # area
            if spu in choashi:
                area = final_res.get(spu, "")
                for key in area.keys():
                    item = {
                        "url": f"https://detail.tmall.com/item.htm?id={spu}&skuId={sku}",
                        "sku": sku,
                        "spu": spu,
                        "shop_name": shop_name,
                        "product_name": product_name,
                        "product_params": "",
                        "original_price": "",
                        "prom_price": spu_price,
                        "promotion": promotion,
                        "prom_activity": prom_activity,
                        "stock": spu_stock,
                        "status": status,
                        "area": f"{key}|{area[key]}",
                    }
                    res_li.append(item)
            else:
                item = {
                    "url": f"https://detail.tmall.com/item.htm?id={spu}&skuId={sku}",
                    "sku": sku,
                    "spu": spu,
                    "shop_name": shop_name,
                    "product_name": product_name,
                    "product_params": "",
                    "original_price": "",
                    "prom_price": spu_price,
                    "promotion": promotion,
                    "prom_activity": prom_activity,
                    "stock": spu_stock,
                    "status": status,
                    "area": "",
                }
                res_li.append(item)

            # item = {
            #     "url": f"https://detail.tmall.com/item.htm?id={spu}&skuId={sku}",
            #     "sku": sku,
            #     "spu": spu,
            #     "shop_name": shop_name,
            #     "product_name": product_name,
            #     "product_params": "",
            #     "original_price": "",
            #     "prom_price": spu_price,
            #     "promotion": promotion,
            #     "prom_activity": prom_activity,
            #     "stock": spu_stock,
            #     "status": status,
            #     "area": "",
            # }
            # res_li.append(item)

    to_excel("tmall", res_li)


def export_jd():
    dis_li = []
    detail_li = jd_goods_detail.find({"status": {"$exists": True}})
    res_li = []
    for detail in detail_li:
        sku = detail["sku"]
        shop_name = detail["shop_name"]
        product_name = detail["title"]
        product_params = detail["sale_prop"]
        status = detail.get("status", "")
        if sku in dis_li:
            continue
        dis_li.append(sku)

        # price
        price = jd_goods_price.find_one({"sku": sku})
        if price:
            original_price = price.get("data", {}).get("op", "")
            prom_price = price.get("data", {}).get("p", "")
        else:
            original_price = ""
            prom_price = ""

        # promotion
        promotion = jd_goods_promotion.find_one({"sku": sku})
        if promotion:
            name = promotion.get("data", {}).get("name", "")
            timeDesc = promotion.get("data", {}).get("timeDesc", "")
            trueDiscount = promotion.get("data", {}).get("trueDiscount", "")
            quota = promotion.get("data", {}).get("quota", "")
            promotion = f"{name}|{timeDesc}|{trueDiscount}|{quota}"
        else:
            promotion = ""

        # prom
        prom = jd_goods_prom.find_one({"sku": sku})
        if prom:
            icon_text = prom.get("gift", {}).get("nm", "")
            title = prom.get("gift", {}).get("num", "")
            prom_activity = f"{icon_text}|{title}"
        else:
            prom_activity = ""

        item = {
            "url": f"https://item.jd.com/{sku}.html",
            "sku": sku,
            "shop_name": shop_name,
            "product_name": product_name,
            "product_params": product_params,
            "original_price": original_price,
            "prom_price": prom_price,
            "promotion": promotion,
            "prom_activity": prom_activity,
            "stock": "",
            "status": status
        }
        res_li.append(item)
    to_excel("jd", res_li)


def to_excel(excel_name, li):
    df = pd.DataFrame(li)
    # df.to_csv(f'{excel_name}.csv', mode='a')
    df.to_excel(f'{excel_name}.xlsx')


if __name__ == '__main__':
    export_tmall()
    # export_jd()
