import csv

def check_rhymes(chars: list[dict]) -> list[int]:
    body = [22, 24, 26, 15, 17, 19, 8, 10, 12, 1, 3, 5]
    half_body = [1, 5, 10, 17, 22, 26]
    foot = [6, 13, 20, 27]
    rhymed = [27, 20, 6]
    type = 0

    rhymes = []
    results = []
    for char in chars:
        rhymes.append(char['rhyme'])
        results.append(0)

    for n in body:
        if rhymes[n] == "":
            continue
        elif (rhymes[n].startswith("p")) ^ (n in half_body):
            type = -1
            break
        else:
            type = 1
            break
    print(type)

    if(type != 0):
        for n in body:
            if rhymes[n] == "":
                continue
            elif (rhymes[n].startswith("p") ^ (n in half_body)) ^ (type == -1):
                results[n] += 100
    
    for n in rhymed:
        if(rhymes[n] != "" and not rhymes[n].startswith("p")):
            results[n] += 100

    if(rhymes[20] != "" and rhymes[27] != "" and rhymes[20] != rhymes[27]):
        results[20] += 100
    if(rhymes[6] != "" and rhymes[27] != "" and rhymes[6] != rhymes[27]):
        results[6] += 100
    if(rhymes[6] != "" and rhymes[20] != "" and rhymes[6] != rhymes[20]):
        results[6] += 100    

    for n in foot:
        if(rhymes[n-2].startswith("p") and rhymes[n-1].startswith("p") and rhymes[n].startswith("p")):
            results[n-2] += 100
            results[n-1] += 100
            results[n] += 100

    i = 0
    for rhyme in rhymes:
        add = 0
        if (i in body):
            if (i in half_body):
                add = type
            else:
                add = type * -1
        
        if i in rhymed:
            add = 5
        
        if rhyme != "":
            if rhyme.startswith("p"):
                add += 1
            else:
                add += -1
            if i not in body:
                add *= 2
        results[i] += add
        i += 1

    return results

def get_color_by_checked_rhyme(chars: list[dict]) -> list[tuple]:
    checked = check_rhymes(chars)
    result = []
    for unit in checked:
        match unit:
            case 0:
                color = (1, 1, 1, 1)
            case 1:
                color = (1, 1, 0.7, 1)
            case 2:
                color = (1, 1, 0, 1)
            case -1:
                color = (0.6, 0.6, 1, 1)
            case -2:
                color = (0.2, 0.2, 1, 1)
            case 5:
                color = (0.3, 0.7, 0.2, 1)
            case 12:
                color = (0.7, 1, 0, 1)
            case _:
                color = (1, 0, 0, 1)
        result.append(color)
    return result



#test_data = []
#with open('devs/kanshi/rhyme_test.csv', 'r', encoding='utf-8-sig') as f:
#    reader = csv.DictReader(f)
#    for row in reader:
#        test_data.append(row)
#
#print(get_color_by_checked_rhyme(test_data))
            



    