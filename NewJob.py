#!/usr/bin/env ../Python/3.4.3/bin/python3
import os
import glob
import time
import shutil
import datetime
import subprocess
import configparser
import tkinter
import SlurmInfo
import tkinter.ttk as ttk
from tkinter import messagebox
from getpass import getuser
from tkinter import filedialog
import tkinter.ttk as ttk
import os
import subprocess
import tempfile
import subprocess
import tempfile
class NewJobView(tkinter.Frame):
    #base_path = os.path.dirname(os.path.realpath("__file__"))
    base_path = os.path.dirname(os.path.realpath(__file__))
    current_system_user = None
    list_of_account_names = None
    list_of_par_names = None
    window_size = "800x500"
    pad_x = 42
    pad_y = 10
    #PROGRAM_DIR = "/RS/progs/SlurmPythonGUI"
    DEFAULT_PAR_NAME = "debug"
    #TEMPLATES_DIR = PROGRAM_DIR + "/templates/"
    TEMPLATES_DIR = base_path + "/../templates/"
    #TEMPLATES_DIR = '../templates/'
    inc_and_old_browse_added = 0
    input_file_path = None # dont touch it
    old_file_path = None # dont touch it
    inc_files_paths = None # dont touch it
    row_value = 0
    entrys_column = 1
    work_dir_of_gui = None

    def __init__(self, root, window_size):
        #slurm_gui_conf configparser.ConfigParser()

        self.width = int(window_size.split("x")[0])
        self.height= int(window_size.split("x")[1])
        self.current_system_user = getuser()
        config = configparser.ConfigParser()
        config.read("%s/.slurmgui.conf" %(os.getenv('HOME')))
        value = os.popen("sinfo | awk '{print $1}' | grep -v PARTITION | uniq")
        self.read = value.read()
        self.work_dir_of_gui = config['general']["work_directory"]
        tkinter.Frame.__init__(
            self, root,
            width=self.width,
            height=self.height,
        )
        self.columnconfigure(0,pad=250)

        info = SlurmInfo.Get(default_par_name=self.DEFAULT_PAR_NAME)
        self.list_of_account_names = info.accounts()
        self.list_of_par_names = info.par_names()
        if len(self.list_of_account_names) == 0:
            message = "KullanÄ±cÄ± adÄ±nÄ±za baÄŸlÄ± hesap adÄ±nÄ±z bulunamadÄ±. \
LÃ¼tfen sistem yÃ¶neticiniz ile iletiÅŸime geÃ§iniz"
            messagebox.showinfo("Hata", message)
        if len(self.list_of_par_names) == 0:
            message = "KullanÄ±cÄ± adÄ±nÄ±za baÄŸlÄ± bir kuyruk ismi bulunamadÄ±. \
LÃ¼tfen sistem yÃ¶neticiniz ile iletiÅŸime geÃ§iniz"
            messagebox.showinfo("Hata", message)
        self.create_widgets()
        self.grid_widgets()

        self.combobox_of_template_name.bind(
                "<<ComboboxSelected>>",
                lambda x: self.template_selected(self.combobox_of_template_name)
            )
        self.combobox_of_par_name.bind(
                "<<ComboboxSelected>>",
                lambda x: self.get_taskpernode(self.combobox_of_par_name)
            )


    def create_widgets(self):
        self.error_label = tkinter.Label(self, text='')
        self.get_par_template_label = tkinter.Label(self,text="Program seÃ§iniz")

        self.combobox_of_template_name = ttk.Combobox(
            self,
            state="readonly",
            values=tuple(self.get_templates()),
            )
        self.get_job_name_label = tkinter.Label(self, text="Ä°ÅŸ ismi")
        self.get_job_name_entry = tkinter.Entry(self)
        self.get_core_number_label = tkinter.Label(self, text="Core SayÄ±sÄ±")
        self.taskpernode_label = tkinter.Label(self,text = "Task per node")
        self.taskpernode_entry = tkinter.Spinbox(self,from_=1,to=1001)
        self.get_core_number_entry = tkinter.Spinbox(self,from_=1,to=1001)
        self.get_account_name_label = tkinter.Label(self,text="Hesap adÄ±",)
        self.combobox_of_account_name = ttk.Combobox(
            self,
            state="readonly",
            values=tuple(self.list_of_account_names),
        )
        self.get_par_name_label = tkinter.Label(self, text="Kuyruk ismi", )
        self.combobox_of_par_name = ttk.Combobox(
            self,
            state="readonly",
            values=tuple(self.read),
        )
        self.get_input_file_label = ttk.Label(self, text="inp dosyasÄ±", )

        self.browse_button = ttk.Button(
            self,
            text="GÃ¶zat(inp DosyasÄ±)",
            command=lambda:self.browse("input_file")
        )

        self.run_button = ttk.Button(
            self, text="BaÅŸlat",
            command=lambda:self.run(
                self.get_job_name_entry.get(),
                self.get_core_number_entry.get(),
                self.combobox_of_account_name.get(),
                self.combobox_of_par_name.get(),
                self.combobox_of_template_name.get(),
            ),
        )

    def grid_widgets(self):
            self.columnconfigure(0,pad=300)
            self.entrys_column = 2
            self.error_label.grid(
                column=0, columnspan=2,
                row=self.row_value, pady=self.pad_y,
                padx=self.pad_x,
            )
            self.row_value = self.row_value + 1
            self.get_par_template_label.grid(
                column=0, row=self.row_value,
                pady=self.pad_y, padx=self.pad_x,
                sticky="W",
            )

            self.combobox_of_template_name.grid(
                column=self.entrys_column, row=self.row_value,
                pady=self.pad_y, padx=self.pad_x,
                sticky="e"
            )
            self.row_value = self.row_value + 1

            self.get_job_name_label.grid(
                column=0, row=self.row_value,
                pady=self.pad_y, padx=self.pad_x,
                sticky="W",
            )
            self.get_job_name_entry.grid(
                column=self.entrys_column, row=self.row_value,
                pady=self.pad_y, padx=self.pad_x,
            )

            self.row_value = self.row_value + 1
            self.get_core_number_label.grid(
                column=0, row=self.row_value,
                pady=self.pad_y, padx=self.pad_x,
                sticky="W",
            )
            self.get_core_number_entry.grid(
                column=self.entrys_column, row=self.row_value,
                pady=self.pad_y, padx=self.pad_x,
            )

            self.row_value = self.row_value + 1


            self.get_account_name_label.grid(
                column=0, row=self.row_value,
                pady=self.pad_y, padx=self.pad_x,
                sticky="W",
            )
            self.combobox_of_account_name.grid(
                column=self.entrys_column, row=self.row_value,
                pady=self.pad_y, padx=self.pad_x,
            )
            #self.combobox_of_account_name.set(self.list_of_account_names[0])

            self.row_value = self.row_value + 1
            self.get_par_name_label.grid(
                column=0, row=self.row_value,
                pady=self.pad_y, padx=self.pad_x,
                sticky="W"
            )
            self.combobox_of_par_name.grid(
                column=self.entrys_column, row=self.row_value,
                pady=self.pad_y, padx=self.pad_x,
            )
            #self.combobox_of_par_name.set(self.list_of_par_names[0])

            self.row_value = self.row_value + 1

            self.taskpernode_label.grid(
                column=0, row=self.row_value,
                pady=self.pad_y, padx=self.pad_x,
                sticky="W",
                )

            self.taskpernode_entry.grid(
                column=self.entrys_column, row=self.row_value,
                pady=self.pad_y, padx=self.pad_x,
                )

            self.row_value = self.row_value + 1
            
            self.get_input_file_label.grid(
                column=0, row=self.row_value,
                pady=self.pad_y, padx=self.pad_x,
                sticky="W",
            )
            self.browse_button.grid(
                column=self.entrys_column, row=self.row_value,
                pady=self.pad_y, padx=self.pad_x
            )

            self.row_value = self.row_value + 1

            self.run_button.grid(
                column=self.entrys_column, row=999,
                pady=self.pad_y, padx=self.pad_x,
            )
            self.row_value = self.row_value + 1

    def get_templates(self):
        #command = "ls " + self.base_path + self.TEMPLATES_DIR + " | grep .sbatch"
        #raw_data = subprocess.getoutput(command)
        #list_of_sbatchs = []
        command = self.TEMPLATES_DIR + '*.sbatch'
        list_of_sbatchs = glob.glob(command)
        temp = []
        for i in list_of_sbatchs:
            raw = i.split('/')[-1]
            raw = raw.replace('.sbatch','')
            temp.append(raw)

        list_of_sbatchs = temp
        return list_of_sbatchs

    def browse(self,name):
        if name == "input_file":
            self.input_file_path = filedialog.askopenfilename(
                initialdir='~',
                filetypes=(
                    ("Input Files",("*.inp", "*.in")),
                    ("All files", "*.*"),
                )
            )
        elif name == "old_file":
            self.old_file_path = filedialog.askopenfilename(
                initialdir='~',
                filetypes=(
                    ("", "*.odb"),
                )
            )
        elif name == "inc_file":
            self.inc_files_paths = filedialog.askopenfilename(
                initialdir="~",
                filetypes=(
                    ("","*.inc"),
                    ("All files", "*.*"),
                ),
                multiple=True,
            )

    def get_modules(self, template_name):
        config = configparser.ConfigParser()
        config.read('%s/../config/sbatch_modules.conf'%(self.base_path))
        if not template_name in config.sections():
            return 1
        modules = config[template_name]['modules'].split(',')
        if len(modules) == 1 and modules[0] == '':
            return ''
        for i in range(0,len(modules)):
            modules[i] = "module load %s\n" %(modules[i].strip())
        return ''.join(modules)

    def run(
            self,
                job_name,core_number,
                    account_name,par_name,
                        template_name ):
        self.browse_button.config(state=tkinter.DISABLED)
        self.run_button.config(state=tkinter.DISABLED)
        error = None

        if  self.input_file_path == None or not os.path.exists(self.input_file_path):
            error = "LÃ¼tfen geÃ§erli bir input dosyasÄ± giriniz."
        if not self.input_file_path:
            error = "LÃ¼tfen geÃ§erli bir input dosyasÄ± giriniz."
        if not core_number.isnumeric():
            error = "LÃ¼tfen core sayÄ±sÄ±nÄ± rakam olarak giriniz."
        if not template_name:
            error = "LÃ¼tfen program seÃ§iniz"

        modules = self.get_modules(template_name)
        if modules == 1:
            error = "sbatch_modules.conf dosyasÄ±nda ilgili programa ait modÃ¼l \
isimleri bulunamadÄ±. LÃ¼tfen sistem yÃ¶neticisi ile iletiÅŸime geÃ§iniz"

        if error:
            self.error_label.config(text=error)
            self.browse_button.config(state=tkinter.ACTIVE)
            self.run_button.config(state=tkinter.ACTIVE)
            return

        job_files_directory =  self.work_dir_of_gui + "/job_files/"
        error_files_directory = self.work_dir_of_gui + "/error_files/"

        if not os.path.exists(self.work_dir_of_gui):
            os.mkdir(self.work_dir_of_gui)

        if not os.path.exists(job_files_directory):
            os.mkdir(job_files_directory)

        if not os.path.exists(error_files_directory):
            os.mkdir(error_files_directory)

        time_stamp = int(time.time())

        filename_of_template = self.TEMPLATES_DIR + template_name + '.sbatch'
        sbatch_file = open(filename_of_template)
        content_of_template = sbatch_file.read()

        job_directory = job_files_directory + str(time_stamp) + '-' + job_name + '/'

        if not os.path.exists(job_directory):
            os.mkdir(job_directory)

        if "abaqus" in template_name and self.old_file_path:
            temp_old_job = "oldjob=" + self.old_file_path.replace(".odb","")
            content_of_sbatch = content_of_template.format(
                core_number=core_number,
                par_name=par_name,
                account_name=account_name,
                job_name=job_name,
                input_file_path=self.input_file_path,
                taskpernode=self.taskpernode_entry.get(),
                output_path="%s/"%(os.path.dirname(self.input_file_path)),
                error_path=error_files_directory,
                old_job=temp_old_job,
                module_loads=modules,
            )
        elif "converge" in template_name:
            content_of_sbatch = content_of_template.format(
                core_number=core_number,
                par_name=par_name,
                account_name=account_name,
                job_name=job_name,
                taskpernode=self.taskpernode_entry.get(),
                output_path="%s/"%(os.path.dirname(self.input_file_path)),
                error_path=error_files_directory,
                module_loads=modules,
            )
        else:
            content_of_sbatch = content_of_template.format(
                core_number=core_number,
                par_name=par_name,
                account_name=account_name,
                job_name=job_name,
                input_file_path=self.input_file_path,
                taskpernode=self.taskpernode_entry.get(),
                output_path="%s/"%(os.path.dirname(self.input_file_path)),
                error_path=error_files_directory,
                old_job='',
                module_loads=modules,
            )

        if "abaqus" in template_name and self.inc_files_paths:
            for i in self.inc_files_paths:
                if os.path.dirname(i) != os.path.dirname(self.input_file_path):
                    shutil.move(i, os.path.dirname(self.input_file_path))

        path_of_sbatch = os.path.dirname(self.input_file_path) + '/' + template_name + '.sbatch'
        sbatch_of_job = open(path_of_sbatch,'w')
        sbatch_of_job.write(content_of_sbatch)
        sbatch_of_job.close()
        time.sleep(1)

        command = "cd " + os.path.dirname(path_of_sbatch) + " &&" + " sbatch " + path_of_sbatch + ' &'

        result = subprocess.getoutput(command)
        error = result
        messagebox.showinfo("Result", error)

        time.sleep(3)
        self.browse_button.config(state=tkinter.ACTIVE)
        self.run_button.config(state=tkinter.ACTIVE)

    def get_taskpernode(self, cbox):
        par_name = cbox.get()
        command = "sinfo  -o '%%c' -h -p %s" %(par_name)

        result = subprocess.getoutput(command)

        if result == '':
            message = "Kuyruk ismine baÄŸlÄ± node bulunamadÄ±! \
LÃ¼tfen sistem yÃ¶neticiniz ile iletiÅŸime geÃ§iniz"
            messagebox.showinfo("Hata", message)
            return
        self.taskpernode_entry.delete(0,'end')
        self.taskpernode_entry.insert(0, result)

    def template_selected(self,cbox):
        if "abaqus" in cbox.get() and not self.inc_and_old_browse_added:
            self.inc_and_old_browse_added = 1

            self.inc_file_label = ttk.Label(
                self,
                text="inc dosyasÄ±/dosyalarÄ±\n(Opsiyonel)",
                )
            self.inc_file_label.grid(
                column=0,
                row=self.row_value,
                pady=self.pad_y,
                padx=self.pad_x,
                sticky="W",
                )

            self.inc_browse_button = ttk.Button(
                self,
                text="GÃ¶zat(inc dosyasÄ±)",
                command=lambda:self.browse("inc_file")
                )
            self.inc_browse_button.grid(
                column=self.entrys_column, row=self.row_value,
                pady=self.pad_y, padx=self.pad_x,
                )

            self.row_value = self.row_value + 1

            self.old_file_label = ttk.Label(
                self,
                text="Eski iÅŸ dosyasÄ±\n(Opsiyonel)",
                )
            self.old_file_label.grid(
                column=0,
                row=self.row_value,
                pady=self.pad_y,
                padx=self.pad_x,
                sticky="W"
                )

            self.old_file_browse_button = ttk.Button(
                self,
                text="GÃ¶zat(Eski Ä°ÅŸ)",
                command=lambda:self.browse("old_file")
                )
            self.old_file_browse_button.grid(
                column=self.entrys_column, row=self.row_value,
                pady=self.pad_y, padx=self.pad_x,
                )

            self.row_value = self.row_value + 1
        elif "abaqus" in cbox.get() and self.inc_and_old_browse_added:
            pass

        else:
            if hasattr(self, 'old_file_label'):
                self.old_file_label.destroy()
            if hasattr(self, 'old_file_browse_button'):
                self.old_file_browse_button.destroy()
                self.row_value -= 1
            if hasattr(self, 'inc_file_label'):
                self.inc_file_label.destroy()
            if hasattr(self, 'inc_browse_button'):
                self.inc_browse_button.destroy()
                self.row_value -= 1
            self.inc_and_old_browse_added = 0
