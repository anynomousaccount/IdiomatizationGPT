import os, sys
import struct
import traceback

code_dir = "/".join(os.path.abspath(__file__).split("/")[:-2]) + "/"
print("code path: ", code_dir)
sys.path.append(code_dir)
import chatgpt_util, random
import openai, tiktoken, ast, util
import ast, copy

if __name__ == '__main__':
    idiom = "call_star"
    idiom = "_".join(idiom.split(" "))
    save_complicated_code_dir_root = util.data_root + "chatgpt/NonIdiomatic/"
    # save_complicated_code_dir_root = util.data_root + "NonIdiomatic/find_code_snippets/"
    save_complicated_code_dir = save_complicated_code_dir_root + "sample_methods/"
    file_name = "rewrite_instr_from_code_generation.csv"
    file_name = "rewrite_instr_from_code_generation.csv"
    file_name = "rewrite_call_star_from_abstract_same_subscript_value_instr7_all_new_add_cannot_refactor_modify_old_code_new_code_get_acc_add_info_add_cannot_refactor_new.csv"
    # save_complicated_code_dir_root + idiom + "/" + csv_file_name,
    benchmarks = []
    all_res = util.load_csv(save_complicated_code_dir_root + idiom + "/" + file_name)
    # util.save_pkl(save_complicated_code_dir_root + idiom + "/",
    #               "get_acc_res",
    #               csv_res_list)
    csv_res_list_pkl = util.load_pkl(save_complicated_code_dir_root + idiom + "/", "csv_res_list_pkl")

    # repo_name, old_path, file_html, class_name, me_name, method_code, old_code, refactor_code, *other = sample
    flag = 0
    res = []
    for ind_e, e in enumerate(all_res):
        if ind_e == 0:
            continue
        print("len(e): ", len(e))
        print("e: ", e)
        for ind_k, k in enumerate(e):
            print("k", ind_k, k)

        repo_name, old_path, file_html, class_name, me_name, method_code, old_code, chat_gpt_code, element_str, slice_str, ridiom_code, acc, chatgpt_acc, *other = e
        print("csv_res_list_pkl[ind_e-1]: ", csv_res_list_pkl[ind_e - 1])
        ridiom_acc, real_acc = '1', '1'
        if "FOUND" in repo_name:
            flag = 1
            continue
        if not flag:
            repo_name, old_path, file_html, class_name, me_name, method_code, old_code, chat_gpt_code, element_str, slice_str, ridiom_code, *other = \
            csv_res_list_pkl[ind_e - 1]
        else:
            repo_name, old_path, file_html, class_name, me_name, method_code, old_code, ridiom_code, *other = \
            csv_res_list_pkl[ind_e - 1]

        # if not me_name:
        #     continue
        # if "for x in range(TEST_TIMEOUT)" in old_code:
        #     print(acc,real_acc,chatgpt_acc,ridiom_acc)

        acc, real_acc, chatgpt_acc, ridiom_acc = int(acc) if acc.isdigit() else None, int(
            real_acc) if real_acc.isdigit() else None, int(chatgpt_acc) if chatgpt_acc.isdigit() else None, int(
            ridiom_acc) if ridiom_acc.isdigit() else None
        # if "for event_item in user_dict[" in old_code:#for x in range(TEST_TIMEOUT)
        #     print(acc,real_acc,chatgpt_acc,ridiom_acc)

        if not flag:
            # print("acc: ",acc==1,acc=='1',len(e),e[9])
            if acc == 1:
                if real_acc == 0:
                    continue
                # if "for event_item in user_dict[" in old_code:
                #     print("come here")
                res.append(
                    [repo_name, old_path, file_html, class_name, me_name, method_code, old_code, [chat_gpt_code]])
            elif chatgpt_acc == 1:
                if ridiom_acc != 1:
                    res.append(
                        [repo_name, old_path, file_html, class_name, me_name, method_code, old_code, [chat_gpt_code]])
                else:
                    if "Cannot refactor" not in ridiom_code:
                        res.append([repo_name, old_path, file_html, class_name, me_name, method_code, old_code,
                                    [chat_gpt_code, ridiom_code]])
                    else:
                        res.append([repo_name, old_path, file_html, class_name, me_name, method_code, old_code,
                                    [chat_gpt_code]])

            # elif ridiom_acc==1:
            #     res.append([repo_name, old_path, file_html, class_name, me_name, method_code, old_code,
            #                 [ridiom_code]])
        else:
            pass
            res.append([repo_name, old_path, file_html, class_name, me_name, method_code, old_code,
                        [chat_gpt_code]])
    print("len of benchmark: ", len(res))
    # util.save_pkl(save_complicated_code_dir_root + idiom + "/", "loop_else_bench",res)
    util.save_pkl(save_complicated_code_dir_root + idiom + "/", "call_star_bench_new", res)
