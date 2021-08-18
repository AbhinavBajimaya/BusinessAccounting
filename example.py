for i in range(1,37):
        try:
            b=pyBSDate.convert_BS_to_AD(2078,3,i)
        except:
            break;
print(i)