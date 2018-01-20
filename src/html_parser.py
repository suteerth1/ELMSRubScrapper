from bs4 import BeautifulSoup
import re
#import csv
import json

SUBID_RE = re.compile("submission_(\d+)")
DIR = "../data/grades"
OUTPUT = "../data/scores.json"
FIELD_NAMES = "../data/field_name.txt"


def parse_html(html):
    sub_ids = SUBID_RE.findall(html)
    soup = BeautifulSoup(html, "lxml")
    ret = dict()
    name = re.compile("Grades for (.*): C").findall(html)[0]
    ret["s_name"] = name
    for h in soup.find_all(id=["submission_" + i for i in sub_ids]):
        _id = h["id"].split("_")[1]
        for r in soup.find_all(id="rubric_" + _id):
            trs = r.find_all(id=re.compile("criterion__\d+"))
            for tr in trs:
                lab = tr.find(attrs={"class": "criterion_description_value"})
                if lab:
                    lab = lab.string
                    score = list(tr.find("td", class_="nobr points_form").stripped_strings)
                    score = (score[1])  # + "/" + score[3])
                    assn_name = list(h.stripped_strings)[0]
                    lab_bits = lab.split(" ")
                    ret[assn_name[0] + assn_name[-1] + lab_bits[0][0] + lab_bits[1]] = score
    return ret


def process_html(inf, dwriter, keys):
    scores = parse_html(inf.read())
    dwriter.writerow(scores)


if __name__ == "__main__":
    with open(DIR + "/../ids.txt") as lst:
        outf = open(OUTPUT, 'w')
        field_name = [x.strip() for x in open(FIELD_NAMES, 'r').read().split(',')]
        print(field_name)
        #dwriter = csv.DictWriter(outf, fieldnames=field_name)
        #dwriter.writeheader()
        jwriter = outf
        jwriter.write("[\n")
        for html in lst:
            html = html.split("/")[-1]
            id_ = html
            try:
                inf = open(DIR + "/" + html.strip())
                html = inf.read()
                inf.close()
                row = parse_html(html)
                row["s_id"] = id_
                for k in field_name:
                    row[k] = row.get(k, '')
                print("[+] processed " + row["s_name"] + " id:" + row["s_id"])
                #(dwriter.writerow(row))
                j_ = json.dumps(row,  sort_keys=False, indent=4, separators=(',', ': '))
                jwriter.write(j_)
                jwriter.write(",")
            except FileNotFoundError:
                print("[x] File not found")
            except Exception:
                print("[x]"+id_+"Not processed")
        jwriter.write('null]')

        outf.close()
