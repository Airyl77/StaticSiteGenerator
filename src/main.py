from textnode import *
import os
import shutil
import sys

def main():
    #obj_TextNode = TextNode("This is some anchor text", TextType.LINK_TEXTTYPE, "https://www.boot.dev")
    #print(obj_TextNode)
    basepath = sys.argv[1]
    if basepath == "":
        basepath = "/"
    print(f"basepath======>{basepath}")
    #path_pub = "public"
    path_pub = "docs"
    path_stat = "static"
    if os.path.exists(path_pub):
        shutil.rmtree(path_pub)
    os.mkdir(path_pub)
    copy_stat(path_pub, path_stat)
    #generate_page("content/index.md","template.html","public/index.html")
    generate_pages_recursive(basepath,"content","template.html","docs")
        

def copy_stat(path_pub, path_stat):
    #print(f"LBO path_pub={path_pub}, path_stat={path_stat}")
    # if os.path.exists(path_stat) and !os.path.isfile(path_stat):
    list = os.listdir(path_stat)
    for dir in list:
        new_path_stat = os.path.join(path_stat, dir)
        #print(f"LBO dir={dir}")
        if os.path.isfile(new_path_stat):
            shutil.copy(new_path_stat, path_pub)
        else:
            new_path_pub = os.path.join(path_pub, dir)
            new_path_stat = os.path.join(path_stat, dir)
            #print(f"LBO new_path_stat={new_path_stat}, new_path_pub={new_path_pub}")
            os.mkdir(new_path_pub)
            copy_stat(new_path_pub, new_path_stat)
    return

def generate_page(basepath,from_path, template_path, dest_path):
    #print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    f = open(from_path)
    v_f = f.read()
    tf = open(template_path)
    v_tf = tf.read()

    title =extract_title(v_f)
    
    nodes = markdown_to_html_node(v_f)
    #print(f"LBO nodes = {nodes}") 
    nodes_str = nodes.to_html()
    #title =extract_title(nodes_str)

    v_tf_new = v_tf.replace("{{ Title }}", title)
    v_tf_new2 = v_tf_new.replace("{{ Content }}", nodes_str)
    v_tf_new3 = v_tf_new2.replace("href=\"/", f"href=\"{basepath}")
    v_tf_new4 = v_tf_new3.replace("src=\"/", f"src=\"{basepath}")
    #print(f"LBO v_tf_new2 = {v_tf_new2}")

    nf = open(dest_path, "w")
    nf.write(v_tf_new4)
    nf.close()

    f.close()
    tf.close()

def generate_pages_recursive(basepath, dir_path_content, template_path, dest_dir_path):
    print(f"Generating page from {dir_path_content} to {dest_dir_path} using {template_path}")
    if os.path.isfile(dir_path_content):
            split_path = os.path.splitext(dest_dir_path)
            new_dest_dir_path = split_path[0] + ".html"
            generate_page(basepath, dir_path_content, template_path, new_dest_dir_path)
            return
    else:
        if os.path.exists(dest_dir_path):
            shutil.rmtree(dest_dir_path)
        os.mkdir(dest_dir_path)
        
        d_list = os.listdir(dir_path_content)
        
        for dir in d_list:
            new_path_content = os.path.join(dir_path_content, dir)
            new_path_dest = os.path.join(dest_dir_path, dir)
            print(f"1 =======> new_path_content= {new_path_content}, new_path_dest = {new_path_dest}")
            generate_pages_recursive(basepath, new_path_content, template_path, new_path_dest)
        return


if __name__ == "__main__":
    main()