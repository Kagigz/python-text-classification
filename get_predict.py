import text_processing
import model_helpers
import azure_storage_helpers

###############
# GETTING MODEL
###############

# GETTING MODEL FROM BLOB STORAGE

# Blob Storage config
# TODO: replace the values with your own
blobConfig = {
    'ACCOUNTNAME': 'YOUR_STORAGE_NAME',
    'KEY': 'YOUR_KEY',
    'CONTAINER': 'main'
}

# Initializing Blob Storage service
blob_service = azure_storage_helpers.InitializeBlobService(blobConfig)

# Model local path
modelPath = 'model.pkl'

# Getting file from Blob Storage and storing it locally
# Comment out this line if you want to use a local one
azure_storage_helpers.getFile(blobConfig,blob_service,'model.pkl',modelPath)

# Loading model
model = azure_storage_helpers.getModel(modelPath)


#############
# PREDICTIONS
#############

# Sample text to predict a label for
# TODO: Replace it with your own
txt = "Text to get a prediction for"

# Getting a prediction
prediction = model_helpers.getPrediction(txt,model)
