from google.cloud import automl_v1beta1
from google.cloud.automl_v1beta1.proto import service_pb2


# 'content' is base-64-encoded image data.
def get_prediction(content, project_id, model_id):
    """
    get_prediction Get if people are wearing masks

    Given a image content is base 64 encoded format with a auto ml project and model id
    return the if mask or no_mask classifcation based on the content with some prob

    Parameters
    ----------
    content : bytes
        image data as base 64 bytes
    project_id : str
        auto ml project id
    model_id : str
        auto ml model id

    Returns
    -------
    dict
        dict with classification and probs.
    """
    prediction_client = automl_v1beta1.PredictionServiceClient()

    name = f"projects/{project_id}/locations/us-central1/models/{model_id}"
    payload = {"image": {"image_bytes": content}}
    params = {}
    request = prediction_client.predict(name, payload, params)
    return request  # waits till request is returned


if __name__ == "__main__":
    # MODEL_ID = "ICN3966723492690264064"
    # PROJECT_ID = "767032446048"

    # with open("test.jpg", "rb") as ff:
    #     content = ff.read()
    #     print(get_prediction(content, PROJECT_ID, MODEL_ID))
    pass
