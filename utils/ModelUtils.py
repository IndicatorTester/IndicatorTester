class ModelUtils:

    @staticmethod
    def toJson(model):
        return model.model_dump()