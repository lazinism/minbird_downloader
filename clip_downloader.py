import json, requests, urllib3, os
from functools import reduce

forbidden_chars = "%:/\\<>*?？|！\n"
thread_number = 5
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
dl_URL = "https://minbird.kr/static/videos/processed/clips/{0}.mp4"
down_dir = os.getcwd() + "/videos/"
if __name__ == "__main__":
    if not os.path.isdir(down_dir):
        print("videos 폴더가 존재하지 않아 생성합니다.")
        os.mkdir(down_dir)
    cn = input("페이지당 클립 수(cn)를 입력하세요. (0 입력 시 가능한 모든 클립 다운로드): ")
    if cn == "0":
        print("모든 클립을 다운로드합니다.")
        ln=0
    else:
        ln = input("페이지 번호(ln)를 입력하세요.")
    URL = "https://minbird.kr/clipmaker/api?re=clipList&cn={0}&ln={1}".format(cn, ln)
    response = requests.get(URL, verify=False)
    if(response.status_code == 200):
        data = json.loads(response.text)
    else:
        raise Exception('클립메이커 페이지가 정상작동 중이지 않습니다.')
    if cn == "0":
        for k,v in data.items():
            safe_k = reduce(lambda x,y: x.replace(y, "_"), list(forbidden_chars), k)
            safe_v = reduce(lambda x,y: x.replace(y, "_"), list(forbidden_chars), v)
            print("{0} / {1} 다운로드 중...".format(k, v))
            r = requests.get(dl_URL.format(k), verify=False)
            with open(down_dir+"{0}[{1}].mp4".format(safe_v, safe_k), 'wb') as f:
                f.write(r.content)
    else:
        for k,v in data.items():
            if not k == "PAGEALL":
                safe_k = reduce(lambda x,y: x.replace(y, "_"), list(forbidden_chars), k)
                v2 = v["cn"]
                safe_v = reduce(lambda x,y: x.replace(y, "_"), list(forbidden_chars), v2)
                print("{0} / {1} 다운로드 중...".format(k, v2))
                r = requests.get(dl_URL.format(k), verify=False)
                with open(down_dir+"{0}[{1}].mp4".format(safe_v, safe_k), 'wb') as f:
                    f.write(r.content)
    print("다운로드가 완료되었습니다.")
    os.system('pause')
            
