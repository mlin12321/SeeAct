import os, shutil

# This file removes any task directory folders from save_captcha_results that are in website_list.txt.
# This is used

def main():
    with open('captcha_check/data/website_list.txt', 'r') as f:
        web_data = f.read()
    web_data = web_data.split("\n")
    web_data = [site_data.split(",") for site_data in web_data]

    base_dir = "captcha_check/save_captcha_results"

    cat_dict = {}
    
    for datapiece in web_data:
        # print(datapiece)
        website = datapiece[0].strip().replace("_", " ")
        cat = datapiece[1].strip().replace("_", " ")
        url = datapiece[2].strip().replace("_", " ")
        todo_flag = None

        try:
            todo_flag = datapiece[3].strip()
        except:
            pass

        if cat not in cat_dict:
            cat_dict[cat] = []

        cat_dict[cat].append(datapiece)

    for cat in cat_dict:
        cat_dict[cat].sort()

    with open('captcha_check/data/website_save_list.txt', 'w') as f:
        for cat in cat_dict:
            for web_data in cat_dict[cat]:
                website = web_data[0].replace("_", " ")
                cat = web_data[1].replace("_", " ")
                url = web_data[2].replace("_", " ")

                print(f"{website}, {cat}, {url}", file=f)

if __name__ == "__main__":
    main()