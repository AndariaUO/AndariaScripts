import wpf, threading
from System.Windows import Window, Visibility
from System.Windows.Controls import Button
from System.Threading import Thread, ThreadStart, ParameterizedThreadStart, ApartmentState
from Assistant import Engine
from AndariaLib import *

import sys, traceback

#globals
WPFDir = 'C:\\Program Files\\Andaria\\AndariaUO\\Data\\Plugins\\ClassicAssist\\WPF\\RailEditor\\'
RAILS = {}
selectedMacro = -1
selectedRail = -1
selectedPos = -1
grid_edit = -1

importString = ""
pickedFn = None

class RailEditor(Window):
    def UpdateUI(self):
        self.btn_m_Down.IsEnabled = self.lst_macro.SelectedIndex >= 0 and self.lst_macro.SelectedIndex < self.lst_macro.Items.Count - 1
        self.btn_m_Up.IsEnabled = self.btn_m_Rem.IsEnabled = self.btn_m_Export.IsEnabled = self.btn_r_Add.IsEnabled = self.btn_r_Import.IsEnabled = self.btn_r_ImportEUO.IsEnabled = self.lst_macro.SelectedIndex >= 0
        self.btn_r_Up.IsEnabled = self.btn_r_Rem.IsEnabled = self.btn_p_Add.IsEnabled = self.btn_p_AddTargetXY.IsEnabled = self.btn_p_AddPlayerPos.IsEnabled = self.btn_r_Export.IsEnabled = self.lst_rails.SelectedIndex >= 0
        self.btn_r_Down.IsEnabled = self.lst_rails.SelectedIndex >= 0 and self.lst_rails.SelectedIndex < self.lst_rails.Items.Count - 1
        self.btn_p_Rem.IsEnabled = self.grid_pos.SelectedIndex >= 0
        self.btn_p_Up.IsEnabled = self.grid_pos.SelectedIndex > 0
        self.btn_p_Down.IsEnabled = self.grid_pos.SelectedIndex >= 0 and self.grid_pos.SelectedIndex < self.grid_pos.Items.Count - 1
        
    def ShowImportExportWindow(self):
        ti = Thread(ThreadStart(ShowImportExport))
        ti.SetApartmentState(ApartmentState.STA)
        ti.Start()
        ti.Join()
        
    def __init__(self):
        wpf.LoadComponent(self, WPFDir + 'RailEditor.xaml')
        LoadConfig(self)
        self.UpdateUI()
       
    #Macro section
    def btn_m_Add_Click(self, sender, e):
        global RAILS
        macro = self.txt_macro.Text
        self.lst_macro.Items.Add(macro)
        RAILS.append((macro, []))
        SaveConfig()
        
    def btn_m_Up_Click(self, sender, e):
        global RAILS, selectedMacro
        SwapArray(RAILS, self.lst_macro.SelectedIndex, True)
        selectedMacro = self.lst_macro.SelectedIndex - 1
        SaveConfig()
        LoadConfig(self)
        
    def btn_m_Down_Click(self, sender, e):
        global RAILS, selectedMacro
        SwapArray(RAILS, self.lst_macro.SelectedIndex, False)
        selectedMacro = self.lst_macro.SelectedIndex + 1
        SaveConfig()
        LoadConfig(self)
    
    def btn_m_Rem_Click(self, sender, e):
        global RAILS, selectedMacro
        RAILS.pop(self.lst_macro.SelectedIndex)
        selectedMacro = -1
        SaveConfig()
        LoadConfig(self)
        
    def btn_m_Import_Click(self, sender, e):
        global pickedFN, importString
        pickedFN = 0
        self.ShowImportExportWindow()
        self.lst_macro.Items.Add(importString[0])
        RAILS.append((importString[0], importString[1]))
        importString = ""
        SaveConfig()
        
    def btn_m_Export_Click(self, sender, e):
        global RAILS, importString, pickedFN
        pickedFN = 1
        macro = DictifyMacro(RAILS[self.lst_macro.SelectedIndex])
        importString = json.dumps(macro, indent=4, sort_keys=True, ensure_ascii=False)
        self.ShowImportExportWindow()
            
    def lst_macro_changed(self, sender, e):
        global RAILS, selectedRail, selectedPos
        selectedRail = selectedPos = -1
        self.grid_pos.ItemsSource = []
        self.grid_pos.Items.Refresh()
        self.lst_rails.Items.Clear()
        if self.lst_macro.SelectedIndex >= 0:
            for rail in RAILS[self.lst_macro.SelectedIndex][1]:
                self.lst_rails.Items.Add(rail[0])
        self.UpdateUI()
        
    def txtblk_macro_MouseDown(self, sender, e):
        txtblk = sender.Parent.Children[0]
        txtbox = sender.Parent.Children[1]
        txtblk.Visibility = Visibility.Collapsed
        txtbox.Visibility = Visibility.Visible
        txtbox.Text = txtblk.Text
        
    def txtbox_macro_LostFocus(self, sender, e):
        global RAILS
        txtblk = sender.Parent.Children[0]
        txtbox = sender.Parent.Children[1]
        txtblk.Visibility = Visibility.Visible
        txtbox.Visibility = Visibility.Collapsed
        txtblk.Text = txtbox.Text
        RAILS[self.lst_macro.SelectedIndex] = (txtblk.Text, RAILS[self.lst_macro.SelectedIndex][1])
        SaveConfig()
        
    #Rails section
    def btn_r_Add_Click(self, sender, e):
        global RAILS
        rail = self.txt_rails.Text
        self.lst_rails.Items.Add(rail)
        RAILS[self.lst_macro.SelectedIndex][1].append((rail,[]))
        SaveConfig()
        
    def btn_r_Up_Click(self, sender, e):
        global RAILS, selectedRail, selectedMacro
        SwapArray(RAILS[self.lst_macro.SelectedIndex][1], self.lst_rails.SelectedIndex, True)
        selectedMacro = self.lst_macro.SelectedIndex
        selectedRail = self.lst_rails.SelectedIndex - 1
        SaveConfig()
        LoadConfig(self)
        
    def btn_r_Down_Click(self, sender, e):
        global RAILS, selectedRail, selectedMacro
        SwapArray(RAILS[self.lst_macro.SelectedIndex][1], self.lst_rails.SelectedIndex, False)
        selectedMacro = self.lst_macro.SelectedIndex
        selectedRail = self.lst_rails.SelectedIndex + 1
        SaveConfig()
        LoadConfig(self)
    
    def btn_r_Rem_Click(self, sender, e):
        global RAILS, selectedRail
        self.lst_rails.Items.Remove(self.lst_rails.SelectedIndex)
        RAILS[self.lst_macro.SelectedIndex][1].pop(self.lst_rails.SelectedIndex)
        selectedRail = -1
        SaveConfig()
        LoadConfig(self)
            
    def btn_r_Import_Click(self, sender, e):
        global pickedFN, importString
        pickedFN = 2
        self.ShowImportExportWindow()
        self.lst_rails.Items.Add(importString[0])
        RAILS[self.lst_macro.SelectedIndex][1].append(importString)
        importString = ""
        SaveConfig()
        
    def btn_r_ImportEUO_Click(self, sender, e):
        global pickedFN, importString
        pickedFN = 4
        self.ShowImportExportWindow()
        self.lst_rails.Items.Add("Imported from EUO")
        RAILS[self.lst_macro.SelectedIndex][1].append(("Imported from EUO", importString))
        print importString
        importString = ""
        SaveConfig()
        
    def btn_r_Export_Click(self, sender, e):
        global RAILS, importString, pickedFN
        pickedFN = 3
        rail = DictifyRail(RAILS[self.lst_macro.SelectedIndex][1][self.lst_rails.SelectedIndex])
        importString = json.dumps(rail, indent=4, sort_keys=True, ensure_ascii=False)
        self.ShowImportExportWindow()
        
    def lst_rails_changed(self, sender, e):
        global RAILS, selectedPos
        selectedPos = -1
        if self.lst_rails.SelectedIndex >= 0:
            self.grid_pos.ItemsSource = RAILS[self.lst_macro.SelectedIndex][1][self.lst_rails.SelectedIndex][1]
            self.grid_pos.Items.Refresh()
        self.UpdateUI()
        
    def txtblk_rails_MouseDown(self, sender, e):
        txtblk = sender.Parent.Children[0]
        txtbox = sender.Parent.Children[1]
        txtblk.Visibility = Visibility.Collapsed
        txtbox.Visibility = Visibility.Visible
        txtbox.Text = txtblk.Text
        
    def txtbox_rails_LostFocus(self, sender, e):
        global RAILS
        txtblk = sender.Parent.Children[0]
        txtbox = sender.Parent.Children[1]
        txtblk.Visibility = Visibility.Visible
        txtbox.Visibility = Visibility.Collapsed
        txtblk.Text = txtbox.Text
        RAILS[self.lst_macro.SelectedIndex][1][self.lst_rails.SelectedIndex] = (txtblk.Text, RAILS[self.lst_macro.SelectedIndex][1][self.lst_rails.SelectedIndex][1])
        SaveConfig()
            
    #Pos section
    def btn_p_Add_Click(self, sender, e):
        global RAILS
        np = Pos(0,0,0, '')
        RAILS[self.lst_macro.SelectedIndex][1][self.lst_rails.SelectedIndex][1].append(np)
        self.grid_pos.Items.Refresh()
        SaveConfig()
        
    def btn_p_AddPlayerPos(self, sender, e):
        global RAILS
        np = Pos(Engine.Player.X, Engine.Player.Y, Engine.Player.Z, '')
        RAILS[self.lst_macro.SelectedIndex][1][self.lst_rails.SelectedIndex][1].append(np)
        self.grid_pos.Items.Refresh()
        SaveConfig()
        
    def btn_p_AddTargetXY(self, sender, e):
        x = threading.Thread(target=TargetXY)
        x.start()
        x.join()
        if FindAlias("RailPosition"):
            np = Pos(X("RailPosition"), Y("RailPosition"), Z("RailPosition"), Name("RailPosition"))
            RAILS[self.lst_macro.SelectedIndex][1][self.lst_rails.SelectedIndex][1].append(np)
            self.grid_pos.Items.Refresh()
            SaveConfig()
            UnsetAlias("RailPosition")
        
    def btn_p_Up_Click(self, sender, e):
        global RAILS, selectedRail, selectedMacro, selectedPos
        SwapArray(RAILS[self.lst_macro.SelectedIndex][1][self.lst_rails.SelectedIndex][1], self.grid_pos.SelectedIndex, True)
        selectedMacro = self.lst_macro.SelectedIndex
        selectedRail = self.lst_rails.SelectedIndex
        selectedPos = self.grid_pos.SelectedIndex - 1
        self.grid_pos.Items.Refresh()
        SaveConfig()
        
    def btn_p_Down_Click(self, sender, e):
        global RAILS, selectedRail, selectedMacro, selectedPos
        SwapArray(RAILS[self.lst_macro.SelectedIndex][1][self.lst_rails.SelectedIndex][1], self.grid_pos.SelectedIndex, False)
        selectedMacro = self.lst_macro.SelectedIndex
        selectedRail = self.lst_rails.SelectedIndex
        selectedPos = self.grid_pos.SelectedIndex + 1
        self.grid_pos.Items.Refresh()
        SaveConfig()
        
    def btn_p_Rem_Click(self, sender, e):
        global RAILS, selectedPos
        RAILS[self.lst_macro.SelectedIndex][1][self.lst_rails.SelectedIndex][1].pop(self.grid_pos.SelectedIndex)
        selectedPos = -1
        SaveConfig()
        self.grid_pos.Items.Refresh()
        
    def grid_pos_changed(self, sender, e):
        self.UpdateUI()
    
    def grid_pos_edited(self, sender, e):
        global grid_edit
        pos = RAILS[self.lst_macro.SelectedIndex][1][self.lst_rails.SelectedIndex][1][self.grid_pos.SelectedIndex]
        if e.Column.DisplayIndex == 3:
            np = Pos(pos.x, pos.y, pos.z, e.EditingElement.Text)
        else:
            num = int(e.EditingElement.Text) if e.EditingElement.Text.isdigit() else None
            if e.Column.DisplayIndex == 0:
                if num is None:
                    e.EditingElement.Text = pos.x
                    return
                np = Pos(e.EditingElement.Text, pos.y, pos.z, pos.note)
            elif e.Column.DisplayIndex == 1:
                if num is None:
                    e.EditingElement.Text = pos.y
                    return
                np = Pos(pos.x, e.EditingElement.Text, pos.z, pos.note)
            else:
                if num is None:
                    e.EditingElement.Text = pos.z
                    return
                np = Pos(pos.x, pos.y, e.EditingElement.Text, pos.note)
        RAILS[self.lst_macro.SelectedIndex][1][self.lst_rails.SelectedIndex][1][self.grid_pos.SelectedIndex] = np
        SaveConfig()
        
class ImportExport(Window):
    def __init__(self):
        global pickedFN
        wpf.LoadComponent(self, WPFDir + 'ImportWindow.xaml')
        if pickedFN == 0:
            self.btn_ok.Click += self.import_macro
        elif pickedFN == 1:
            self.btn_ok.Click += self.export_macro
        elif pickedFN == 2:
            self.btn_ok.Click += self.import_rail
        elif pickedFN == 3:
            self.btn_ok.Click += self.export_rail
        elif pickedFN == 4:
            self.btn_ok.Click += self.import_EUO
    
    def import_macro(self, sender, e):
        global RAILS, importString
        importString = UndictifyMacro(json.loads(self.txt_import.Text))
        self.Close()
        
    def export_macro(self, sender, e):
        global importString
        importString = ""
        self.Close()
        
    def import_rail(self, sender, e):
        global importString
        importString = UndictifyRail(json.loads(self.txt_import.Text))
        self.Close()
        
    def export_rail(self, sender, e):
        global importString
        importString = ""
        self.Close()
        
    def import_EUO(self, sender, e):
        global importString
        currentIndex = 0
        pos = []
        x = y = z = 0
        for line in self.txt_import.Text.splitlines():
            if line is not "":
                split = line.split(" ")
                coord = split[1][1]
                value = int(split[2])
                index = int(split[1][2:])
                if currentIndex < index:
                    pos.append(Pos(x, y, z, ''))
                    x = y = z = 0
                    currentIndex = index
                if coord == "x":
                    x = value
                elif coord == "y":
                    y = value
                elif coord == "z":
                    z = value
        pos.append(Pos(x, y, z, ''))
                
        importString = pos
        self.Close()

def ShowRailEditor():
    try:
        w = RailEditor()
        w.ShowDialog()
    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print("*** print_tb:")
        traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
        print("*** print_exception:")
        traceback.print_exception(exc_type, exc_value, exc_traceback,limit=2, file=sys.stdout)

def ShowImportExport():
    try:
        global importString
        w = ImportExport()
        w.txt_import.Text = importString
        w.ShowDialog()
    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print("*** print_tb:")
        traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
        print("*** print_exception:")
        traceback.print_exception(exc_type, exc_value, exc_traceback,limit=2, file=sys.stdout)
        
def SwapArray(array, index, up):
    if up:
        newInd = index - 1
    else:
        newInd = index + 1
    swap = array[index]
    array[index] = array[newInd]
    array[newInd] = swap
        
def SaveConfig():
    global RAILS
    SaveRails(RAILS)
    
def TargetXY():
    PromptAlias("RailPosition")

def LoadConfig(window):
    global RAILS, selectedMacro, selectedRail, selectedPos
    RAILS = LoadRails()
    window.lst_macro.Items.Clear()
    for macro in RAILS:
        window.lst_macro.Items.Add(macro[0])
    window.lst_macro.SelectedIndex = selectedMacro
    window.lst_rails.SelectedIndex = selectedRail
    window.grid_pos.SelectedIndex = selectedPos

CheckVersion()
t = Thread(ThreadStart(ShowRailEditor))
t.SetApartmentState(ApartmentState.STA)
t.Start()

t.Join()