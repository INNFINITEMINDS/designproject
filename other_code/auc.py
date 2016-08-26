from util import *
from features import *
from sklearn.metrics import roc_auc_score

#Method to generate ROC curves
def testAUC(svmParamList,testData):

#Sample value 
dataSelector = [['Patient_1',0.5,0.5]]
                
for num, dataSet in enumerate(dataSelector):
    print "Loading train,validation samples:\n",dataSelector[num] 
    features = getAllFeatures();
    #TODO: integrate loadTrainAndValData with load_for_patient
    samples = loadTrainAndValData([dataSet],features,)
    print "Training sample size: ",samples['train'].shape
    print "Validation sample size: ",samples['validation'].shape
    print "Training..."
    svmScore = trainSVM(samples['train'])
    print "Done training. Making Classifications..."

    testSample = samples['validation'] 
    testSamples = pd.concat([testSamples, testSample])    
    print "Test sample size: ",testSample.shape
    
    #TODO: Run model against test samples
    #Generate classification results     
    
    seizureAUC = roc_auc_score(true_labels, target_scores)
    nonSeizureAUC = roc_auc_score(false_labels, target_scores)
    averageAUC = (seizureAUC + nonSeizureAUC) / 2
    
    #TODO: Plotting functions to generate curves
    
    print "Seizure AUC: ", seizureAUC
    print "Non Seizure AUC: ", nonSeizureAUC
    print "Average AUC: ", averageAUC
    print "Done."