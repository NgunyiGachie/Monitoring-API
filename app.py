import os
from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api
from config import config
from database import db
from models import User, EnergyConsumption, EnergyProduction, Forecast
from resources.consumption_resource import ConsumptionResource, ConsumptionByID
from resources.forecast_resource import Forecast, ForecastByID
from resources.production_resource import ProductionResource, ProductionByID
from resources.user_resource import us, UserByID

app = Flask(__name__)

config_name = os.getenv("FLASK_CONFIG", "default")
app.config.from_object(config[config_name])

db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)

#registering resources
api.add_resource(ConsumptionResource, "/consumptions", endpoint="consumptions")
api.add_resource(ConsumptionByID, "/consumptions/<int:id>", endpoint="consumptions_by_id")
api.add_resource(Forecast, "/forecasts", endpoint="forecasts")
api.add_resource(ForecastByID, "/forecasts/<int:id>", endpoint="forecasts_by_id")
api.add_resource(ProductionResource, "/productions", endpoint="productions")
api.add_resource(ProductionByID, "/productions/<int:id>", endpoint="productions_by_id")
api.add_resource(USU)

if __name__ == '__main__':
    try:
        port = int(os.environ.get("PORT", 5555))
        app.run(host='0.0.0.0', port=port, debug=True)
    except (ValueError, RuntimeError) as e:
        print(f"An error occurred: {e}")
