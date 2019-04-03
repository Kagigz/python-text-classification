import text_processing
import model_helpers
import azure_storage_helpers

##################
# BUILDING DATASET
##################

# GETTING CONTENT FROM COSMOSDB

# CosmosDB config
# TODO: replace the values with your own (if you don't have a partition key, leave blank)
cosmosConfig = {
    'ENDPOINT': 'YOUR_ENDPOINT',
    'PRIMARYKEY': 'YOUR_PRIMARY_KEY',
    'DATABASE': 'data',
    'COLLECTION': 'documents',
    'PARTITIONKEY': 'name'
}

# Initializing Cosmos client
cosmosClient = azure_storage_helpers.InitializeCosmosClient(cosmosConfig)

# Getting the contents of all documents in the specified collection
documents = azure_storage_helpers.ReadDocuments(cosmosClient,cosmosConfig)
 
# EXTRACTING CONTENT OF INTEREST
# In this sample, it is supposed that the text is stored as sections inside of pages

# Will contain all the rows to be put in a csv file
data = []

# Column names
firstRow = ['text','label']
data.append(firstRow)

for doc in documents:
    pages = doc.get('pages')
    for page in pages:
        sections = page['sections']
        for section in sections:
            text = section['text']
            text = text_processing.normalizeText(text)
            label = section['label']
            row = [text,label]
            data.append(row)


#################
# STORING DATASET
#################

# Creating CSV file
azure_storage_helpers.createCSV(data,'csvdataset.csv')

# Blob Storage config
# TODO: replace the values with your own
blobConfig = {
    'ACCOUNTNAME': 'YOUR_STORAGE_NAME',
    'KEY': 'YOUR_KEY',
    'CONTAINER': 'main'
}

# Initializing Blob Storage service
blob_service = azure_storage_helpers.InitializeBlobService(blobConfig)


# Uploading dataset to Blob Storage
azure_storage_helpers.uploadFile(blobConfig,blob_service,'dataset.csv','csvdataset.csv')


################
# TRAINING MODEL
################

# GETTING DATASET

datasetPath = "csvdataset.csv"

# Getting the dataset from blob storage
# Comment out this line if you want to use a local one
azure_storage_helpers.getFile(blobConfig,blob_service,'dataset.csv','csvdataset.csv') 

# Creating the pandas dataframe
df = model_helpers.createDataframe(datasetPath)


# SPLITTING DATASET
train, test = model_helpers.split(df)


# CREATING PIPELINE
pipe = model_helpers.createPipeline()


# TRAINING
train1 = train['text'].tolist()
labelsTrain1 = train['label'].tolist()
pipe.fit(train1, labelsTrain1)


# TESTING
test1 = test['text'].tolist()
labelsTest1 = test['label'].tolist()
preds = pipe.predict(test1)
accuracy = model_helpers.getAccuracy(labelsTest1,preds)
print("Accuracy:", accuracy)


######################
# SAVING TRAINED MODEL
######################

# Uploads trained model to Blob Storage as well and saves it locally
azure_storage_helpers.uploadPickle(blobConfig,blob_service,pipe,"model.pkl","model.pkl")