import re;

class Filter:
    
    def __init__(self, \
                 keyWords, \
                 attributes, \
                 conditions) :
        '''
            keyWords = list of strings to be searched for in tweets.
            attributes = list of strings with attributes the tweets have to fulfill
            conditions = list of list of strings, corresponding to the attributes.
                            the conditions have to be fulfilled looking at the attributes
        '''
        self.keyWords = keyWords;
        self.attributes = attributes;
        self.conditions = conditions;
        self.keywordDict = self.createKeywordDict();   
    
    def createKeywordDict(self) :
        if self.keyWords != None and len(self.keyWords) > 0 : 
            res = dict.fromkeys(self.keyWords);
            for key in self.keyWords :
                res[key + "s"] = None;
                res[key + "'s"] = None;
            return res;
        else :
            return None;
        
    def getValuesForKey(self, d, key) :
        '''
            Searches an entire (nested) dictionary for a key and 
            returns its value or None.
        '''
        # case : key is part of the current level of the dict.
        if key in d : return d[key];
        
        for _, v in d.iteritems() :            
            # case : v is dictionary
            if isinstance(v, dict):
                res = self.getValuesForKey(v, key);
                if res != None : return res;
                
            # case : v is a list
            elif type(v) is list:
                for entry in v :
                    if isinstance(entry, dict):
                        res = self.getValuesForKey(entry, key);
                        if res != None : return res;
                
        return None;
        
    def evalDict(self, dic) :
        # (1) check the attributes of the dic
        if self.attributes != None and len(self.attributes) > 0 :
            for aIdx in range(len(self.attributes)) :
                # only look for the attribute if it exists in the dic:
                val = self.getValuesForKey(dic, self.attributes[aIdx]);
                
                # case : dict has the attribute
                if val != None :
                    # if no condition is fulfilled, skip.
                    if not (val in self.conditions[aIdx]) :
                        return False;
                # case: dic does not have the attribute
                else :
                    return False;
                
        # (2) check whether the text of the dic fulfills the context.
        if self.keyWords != None and len(self.keyWords) > 0 : 
            h = False;
            for word in dic["text"].split() :
                if word.lower() in self.keywordDict :
                    h = True;
                    break;
            if not h : return False;
        
        return True;

def loadRowsAsList(path = None) :
    '''
        loads the rows of the file located at path
        as string list.
    '''
    if path == None :
        return None;
    
    res = [];
    with open(path) as f :
        for line in f :
            res.append(line.strip().lower());
            
    return res;


        
    
        
        