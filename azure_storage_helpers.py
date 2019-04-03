import azure.cosmos.cosmos_client as cosmos_client
from azure.storage.blob import BlockBlobService, PublicAccess
import csv
import pickle


# Initializes CosmosDB Client
def InitializeCosmosClient(config):
    client = cosmos_client.CosmosClient(url_connection=config['ENDPOINT'], auth={'masterKey': config['PRIMARYKEY']})
    return client


# Reads all documents in the given collection
def ReadDocuments(client,config):
        collection_link = 'dbs/'+ config['DATABASE'] + '/colls/' +  config['COLLECTION']
        documentlist = list(client.ReadItems(collection_link))     
        print('Found {0} documents'.format(documentlist.__len__()))
        documents = []
        for doc in documentlist:
            docId = doc.get('id')
            pk = doc.get(config['PARTITIONKEY'])
            documents.append(ReadDocument(docId,pk,client,collection_link))
        return documents


# Reads the contents of a document            
def ReadDocument(doc_id,pk,client,collection_link): 
        doc_link = collection_link + '/docs/' + doc_id
        if pk != '':
            response = client.ReadItem(doc_link,{'partitionKey':pk})
        else:
            response = client.ReadItem(doc_link)
        print('Read document {0}'.format(response.get('name')))
        return response


# Initializes Blob Storage Service
def InitializeBlobService(config):
    service = BlockBlobService(account_name=config['ACCOUNTNAME'], account_key=config['KEY'])
    return service

# Uploads file to Blob Storage
def uploadFile(config,service,filename,f):
    try:
        service.create_blob_from_path(config['CONTAINER'], filename, f)
        print("File uploaded to blob storage.")
    except Exception as e:
        print(e)

# Creates CSV file
def createCSV(data,filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csvFile:
        writer = csv.writer(csvFile,delimiter='|')
        writer.writerows(data)
        csvFile.close()
        print("CSV file created.")

# Gets file from Blob Storage and stores it locally
def getFile(config,service,filename,path):
    try:
        service.get_blob_to_path(config['CONTAINER'], filename, path)
        print("File retrieved from blob storage.")
    except Exception as e:
        print(e)

# Creates a pickle file, saves it locally, and uploads it to Blob Storage
def uploadPickle(config,service,data,filename,path):
    with open(path, 'wb') as f:  
        pickle.dump(data, f)
        print("Pickle file created.")
    uploadFile(config,service,filename,path)  

# Loads model from local file
def getModel(path):
    model = pickle.load(open(path, 'rb'))
    print("Model loaded.")
    return model