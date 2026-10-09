import numpy as np
import os 
import pandas as pd


class DataLoader:
    def __init__(self):
        self.data, self.subjects= self.dataLouder()
        self.EnrNums = self.EnrNumInd(self.data)
        self.Names = self.NameInd(self.data)
        self.DataSplitBySubject , self.TotalMarksBysub = self.dataSplitBySubject()
        self.DataSplitBySubject = self.DataCleaning()
        

    
    def TotalMark(self,sem):
        TotalMark = np.zeros(shape=(self.data[sem].shape[0])) 
        for subject in self.subjects[sem]:
            TotalMark = TotalMark + self.TotalMarksBysub[sem][subject]

        

        return TotalMark
             
    def averageMark(self,indexes, sem):
        avgMark = np.mean(self.TotalMark(sem)[indexes])
        return avgMark
        

    def dataLouder(self):
        os.chdir(r"C:\Users\prant\OneDrive\Desktop\Python project\main\data")
        lestOfSemesters = os.listdir()
        data = {}
        subjects = {}
        for semester in lestOfSemesters:
            os.chdir(semester)
            
            semesterData = pd.read_csv("marks.csv")
            f = open("subjects.txt", "r")
            subjectsList = f.read().split()
            f.close()
        
            subjects[semester] = subjectsList

            npSemesterData = np.array(semesterData)
            data[semester] = npSemesterData
            os.chdir("..")
        os.chdir("..")
            


        return data , subjects
    
    def DataCleaning(self):

        CDataSplitBySubject = {}
        for sem, subjects in self.DataSplitBySubject.items():
            CDataSplitBySubject[sem] = {}
            for subject, marks in subjects.items():
                CDataSplitBySubject[sem][subject] = {}

                for Test,mark in marks.items():
                    

                    clean_marks = np.where(mark=="AB", 0, mark)
                

                    CDataSplitBySubject[sem][subject][Test] = clean_marks.astype('f')

    
        return CDataSplitBySubject

    # Filtering

    def filterByBranchIndex(self, sem, branch):

        BranchData = np.where(self.data[sem][:,2]==branch)[0]

        return BranchData
    
    def filterByDepartmentIndex(self, sem, Department):

        DepartmentData = np.where(self.data[sem][:,1]==Department)[0]

        return DepartmentData

    def filterByBatchIndex(self, sem, batch):

        BatchdData = np.where(self.data[sem][:,5]==batch)[0]

        return BatchdData

    def filterByMentorIndex(self, sem, Mentor):

        MentorData = np.where(self.data[sem][:,7]==Mentor)[0]

        return MentorData

    def filterByMediumOfSchoolingIndex(self, sem, Medium):

        MediumData = np.where(self.data[sem][:,-1]==Medium)[0]

        return MediumData

    def IndexsToData(self, sem, Indexs):


        data = self.data[sem][Indexs]

        return data
    
    # Searching

    def EnrNumInd(self,data):
        EnrNumDic = {}
        for semester, data in data.items():
            EnrNumDic[semester] = {}
            for i,record in enumerate(data):
                EnrNumDic[semester][record[4]] = i
        return EnrNumDic
    
    def NameInd(self,data):
        NameDic = {}
        for semester, data in data.items():
            NameDic[semester] = {}
            for i,record in enumerate(data):
                NameDic[semester][record[6]] = i
        return NameDic

    def SearchByEnrNum(self, sem, Enr):
        EnrNumDic = self.EnrNums
        ind = EnrNumDic[sem][Enr]
        return self.data[sem][ind]
    
    def SearchByName(self, sem, name):
        NameDic = self.Names

        ind = NameDic[sem][name]
        return self.data[sem][ind]
    
    def dataSplitBySubject(self):
        DataBySubject = {}
        TotalMarks = {}

        for sem, data in self.data.items():
            DataBySubject[sem] = {}
            TotalMarks[sem] = {}
            subjects = self.subjects[sem]
            for i, subject in enumerate(subjects):
                DataBySubject[sem][subject] = {}
                TotalMarks[sem][subject] = data[:, i*5+12]
                for j, Test_n in enumerate(["Test-1", "Test-2", "Test-3", "Test-4"]):

                
                    DataBySubject[sem][subject][Test_n] = data[:, i*5+8+j]

        return DataBySubject , TotalMarks
    

    def uniqueCategory(self,sem, dataColumns):

        unique, counts = np.unique(dataColumns, return_counts=True)
        TypeCounts = dict(zip(unique, counts))

        TypeCounts = dict(sorted(TypeCounts.items(), key=lambda item: item[1], reverse=True))


        return list(TypeCounts.keys()), list(TypeCounts.values())

    def Mark_distribution(self, SubMarkMatrix,subjects,start=0,end=100,step = 1):

        
        MarkRange = np.arange(start, end + step, step)
        
    
        chart_data = {}
        chart_data["Marks"] = MarkRange
    
        for subject in subjects:
            marks = SubMarkMatrix[subject]

            
            counts = [0] * len(MarkRange)

            
            for m in marks:
                
                counts[int(m/step)] += 1

            chart_data[subject] = counts
    
        return chart_data
