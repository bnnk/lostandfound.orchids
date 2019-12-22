import os,time,random,re
import webbrowser as wb
from flask import Flask, render_template, request
from datetime import datetime as d
import time
app = Flask(__name__, template_folder='templates')
class Items:
    index=0
    def __init__(self):
        self.time = []
        self.count = len(self.time)
    def inc(self):
        self.count += 1
        self.time.append(time.asctime(d.now().utctimetuple()))
    def get(self):
        return self.time
    def dec(self,index):
        self.count -= 1
        del self.time[index]
    def __call__(self):
        pass
BranchList=['BTM Layout','CV Raman Nagar','Jalahalli','Sarjapur','Rajaji Nagar','Sahakar Nagar']
ReportList = ['Report']
ClassList = ['Nursery','K1','K2','I','II','III','IV']
OtherAreas = ['Computer_Lab', 'Swimming_Pool', 'Dispersal_Area', 'Skating_Rink', 'Bus_Area', 'PlayGround','office_room']
ClassList.extend(OtherAreas)
SectionList = ['A','B','C','D','E']
ItemList = ["Bottle", "Bag", "LunchBox","PenPencil","Jacket",'Books','Notebooks','Computer_kit','Shoes','Skating_Kit','Others']
v = [BranchList[0],ClassList]
#Item List
TotalItemCount = [0 for i in ItemList]
TotalItemList = dict(zip(ItemList, TotalItemCount))

BranchWise={}
BranchClassWise={}
BranchClassSectionWise={}

list2 = [ "".join(i.split()) for i in BranchList]
@app.route('/',methods=['GET','POST','PUT'])
def homepage_base():
    return render_template('redirector.html',list = ['Lost','Found'],len = 2, type = ['Lost','Found'] , page = 'main-page')
@app.route('/main-page',methods=['GET','POST','PUT']) 
def mainpage_base():
    reqtype=re.split("\[", request.form['choosen'])
    if reqtype[0] == 'Found':
        return render_template('redirector.html',list = ReportList,len = len(ReportList), type = ReportList, page = 'branch-page')
    else:
        return render_template('redirector.html',list = BranchList,len = len(BranchList), type = list2, page = 'branch-page')
@app.route('/branch-page',methods=['GET','POST','PUT'])
def redirect_branch():
    global BranchClassSectionWise
    branch=re.split("\[", request.form['choosen'])
    if branch[0] == 'Report':
        Branch=[]
        Class=[]
        Section=[]
        Item=[]
        ItemCount=[]
        v = list(BranchClassSectionWise.items())
        vs = sorted(v, key = lambda val: val[0])
        BranchClassSectionWise = dict(vs)
        for i,v in BranchClassSectionWise.items():
            elem=i.split(":")
            Branch.append(elem[0])
            Class.append(elem[1])
            Section.append(elem[2])
            Item.append(elem[3])
            ItemCount.append(v)
        return render_template('Items_consolidated.html', len=len(BranchClassSectionWise), listb=Branch, listbc=Class, listbcs=Section, listbcsi=Item, timeobj=ItemCount)             
    else:
        return render_template('redirector.html',list = ClassList,len = len(ClassList), type = ClassList, page = 'class-page', chosen = branch[0]+":")
@app.route('/class-page',methods=['GET','POST','PUT'])
def redirect_branch_class():
    branch_class=re.split("\[", request.form['choosen'])
    stre =  str(branch_class).split(':')[1].split('\'')[0]
    if stre in OtherAreas:
         return render_template('redirector.html',list = ItemList,len = len(ItemList), type = ItemList, page = 'alert-page', chosen = branch_class[0]+":")   
    return render_template('redirector.html',list = SectionList,len = len(SectionList), type = SectionList, page = 'section-page', chosen = branch_class[0]+":")
@app.route('/section-page',methods=['GET','POST','PUT'])
def redirect_branch_class_section():
    branch_class_section=re.split("\[", request.form['choosen'])
    return render_template('redirector.html',list = ItemList,len = len(ItemList), type = ItemList, page = 'alert-page', chosen = branch_class_section[0]+":")
@app.route('/alert-page',methods=['GET','POST','PUT'])
def redirect_branch_class_section_choice():
    final_choice=re.split("\[", request.form['choosen'])
    b = final_choice[0].split(':')
    try:
        TotalItemList[b[3]] = TotalItemList[b[3]] + 1
    except Exception:
        b.insert(2,'N/A')
        TotalItemList[b[3]] = TotalItemList[b[3]] + 1
    if b[0]+":"+b[2] not in BranchWise.keys():
        BranchWise.update({b[0]+":"+b[2]:0})
    BranchWise[b[0]+":"+b[2]] =  BranchWise[b[0]+":"+b[2]] + 1
    if b[0]+":"+b[1]+":"+b[2] not in BranchClassWise.keys():
        BranchClassWise.update({b[0]+":"+b[1]+":"+b[2]:0})
    BranchClassWise[b[0]+":"+b[1]+":"+b[2]] = BranchClassWise[b[0]+":"+b[1]+":"+b[2]] + 1
    if ':'.join(b) not in BranchClassSectionWise.keys():
        BranchClassSectionWise.update({':'.join(b):Items()})
    BranchClassSectionWise[':'.join(b)].inc()
    return render_template('Items.html', len = len(TotalItemList),list = list(TotalItemList.keys()), value = list(TotalItemList.values()))
@app.route('/delete',methods=['GET','POST','PUT'])
def deleteentry():
    final_choice=re.split("\[", request.form['choosen'])
    bac = final_choice[0].split('|')
    for b in bac:
        b = b.split(":")
        if (len(b[0]) != 0):
            TotalItemList[b[3]] = TotalItemList[b[3]] - 1
            BranchWise[b[0]+":"+b[2]] = BranchWise[b[0]+":"+b[2]] - 1
            BranchClassWise[b[0]+":"+b[1]+":"+b[2]] = BranchClassWise[b[0]+":"+b[1]+":"+b[2]] - 1
            BranchClassSectionWise[':'.join(b[0:4])].dec(int(b[4]))
    return render_template('redirector.html',list = BranchList,len = len(BranchList), type = list2, page = 'branch-page')
@app.errorhandler(500)
def test(e):
    return str(e) + 'Internal Server Error'
print(app.config)
app.run(host = '0.0.0.0',port = '6060')