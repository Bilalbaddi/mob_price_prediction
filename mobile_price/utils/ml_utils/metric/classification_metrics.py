from mobile_price.exception.exception import PricingException
from mobile_price.logging.logger import logging
from mobile_price.entity.artifact_entity import ClassificationMetricArtifact
from sklearn.metrics import recall_score, precision_score, f1_score, accuracy_score, confusion_matrix
import sys


def get_classification_metrics(y_true,y_pred) -> ClassificationMetricArtifact:
    try:
        f1_scores : float= f1_score(y_true,y_pred,average='macro')
        precision : float = precision_score(y_true,y_pred,average='macro')
        recall = recall_score(y_true, y_pred,average='macro')
        logging.info(f"F1 Score: {f1_scores}, Precision: {precision}, Recall: {recall}")

        classification_report = ClassificationMetricArtifact(
            f1_score=f1_scores,
            precision_score=precision,
            recall_score=recall
        )
        return classification_report
    except Exception as e:
        raise PricingException(e,sys) from e