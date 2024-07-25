import os, shutil

# This file removes any task directory folders from save_captcha_results that are in website_list.txt.
# This is used

def main():
    with open('captcha_check/data/website_list.txt', 'r') as f:
        web_data = f.read()
    web_data = web_data.split("\n")
    web_data = [site_data.split(",") for site_data in web_data]

    # with open('captcha_check/data/website_list.txt', 'r') as f:
    #     web_data_save = f.read()
    # web_data_save = web_data_save.split("\n")
    # web_data_save = [site_save_data.split(",") for site_save_data in web_data_save]

    base_dir = "captcha_check/save_captcha_results"

    for datapiece in web_data:
        # print(datapiece)
        website = datapiece[0].strip().replace(" ", "_")
        cat = datapiece[1].strip().replace(" ", "_")
        url = datapiece[2].strip().replace(" ", "_")

        if datapiece not in web_data:
            print(datapiece)
    #print(web_data_save)


if __name__ == "__main__":
    main()