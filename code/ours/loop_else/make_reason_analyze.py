import os, sys
import struct
import traceback

code_dir = "/".join(os.path.abspath(__file__).split("/")[:-2]) + "/"
print("code path: ", code_dir)
sys.path.append(code_dir)
import chatgpt_util, random
import openai, tiktoken, ast, util
import ast,copy


if __name__ == '__main__':
    idiom = "loop_else"
    save_complicated_code_dir_root = util.data_root + "chatgpt/NonIdiomatic/"
    # save_complicated_code_dir_root = util.data_root + "NonIdiomatic/find_code_snippets/"
    save_complicated_code_dir = save_complicated_code_dir_root + "sample_methods/"
    file_name="which_statement_will_execute_4_improve_2_all_new_get_acc_new_add_continue_instr3_add_new_found_new.csv"

    # save_complicated_code_dir_root + idiom + "/" + csv_file_name,
    benchmarks = []
    all_res = util.load_csv(save_complicated_code_dir_root + idiom + "/" +file_name)

    gpt_wrong_list,gpt_new_find_list, gpt_no_find_list=[],[],[]
    # repo_name, old_path, file_html, class_name, me_name, method_code, old_code, refactor_code, *other = sample
    flag = 0
    res = []
    for ind_e, e in enumerate(all_res):

        if ind_e==0:
            continue
        # print("len(e): ",len(e))
        # print("e: ",e)
        # for ind_k,k in enumerate(e):
        #     print("k",ind_k,k)

        repo_name, old_path, file_html, class_name, me_name, method_code, old_code, chat_gpt_code,abstract_code, ridiom_code, acc, chatgpt_acc,ridiom_acc,real_acc,*other=e
        if "FOUND" in repo_name:
            flag=1
            continue
        if acc=="-1":
            acc="2"
        acc,real_acc,chatgpt_acc,ridiom_acc=int(acc) if acc.isdigit() else None,int(real_acc) if real_acc.isdigit() else None, int(chatgpt_acc) if chatgpt_acc.isdigit() else None,int(ridiom_acc) if ridiom_acc.isdigit() else None
        # if "for event_item in user_dict[" in old_code:#for x in range(TEST_TIMEOUT)
        #     print(acc,real_acc,chatgpt_acc,ridiom_acc)
        print("acc,real_acc,chatgpt_acc,ridiom_acc: ", acc,chatgpt_acc,ridiom_acc,real_acc,ridiom_code)
        if not flag:
            # print("acc: ",acc==1,acc=='1',len(e),e[9])
            if acc==0:
                if chatgpt_acc!=1:
                    gpt_wrong_list.append(e)
            elif acc==2 or "Cannot refactor" in ridiom_code:
                if chatgpt_acc==1:
                    gpt_new_find_list.append(e)
                else:
                    gpt_wrong_list.append(e+["it actually cannot refactor"])

        else:
            pass
            gpt_no_find_list.append(e)
    res=all_res[:1]+[["find_or_refactor_wrong"]]+gpt_wrong_list+[["new_find"]]+gpt_new_find_list+[["no_find"]]+gpt_no_find_list
    print("len of benchmark: ",len(res))

    # util.save_pkl(save_complicated_code_dir_root + idiom + "/", "loop_else_bench",res)
    # util.save_pkl(save_complicated_code_dir_root + idiom + "/", "reason_analyze_new",res)
    util.save_csv(
        save_complicated_code_dir_root + idiom + "/" + "reason_analyze_"+idiom + ".csv",
        res)
