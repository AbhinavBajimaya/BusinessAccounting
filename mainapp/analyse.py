from mainapp import models

#get report of item sales by item types as a dictionary


def getreportbytype():

    sale_list={}

    item_types=models.Item_type.objects.all()
    for item in item_types:
        sale_list[item.name]=0

    allsaleitems=models.sale_item.objects.all()
    for i in allsaleitems:
        sale_list[i.items.item_type.name] += i.total_price
    return sale_list










