#USE CUDAENV ANACONDA ENVIRONMENT!!!!!!!
import streamlit as st
import pandas as pd
import bz2
import pickle
import _pickle
import base64
from PIL import Image
import xgboost
#model_name = "autoscout_rf_model.pkl"
import os
#model_namee = "autoscout_rf_model.pkl"
model_namee = "autoscout_rf_compressed_model.pkl.pbz2"
#modell = xgboost.Booster(model_file = 'xg_pipe_model.pkl')
here = os.path.dirname(os.path.abspath(__file__))
model_name = os.path.join(here, model_namee)
def decompress_pickle(file):
	data = bz2.BZ2File(file, 'rb')
	data = _pickle.load(data)
	return data
model = decompress_pickle(model_name)
#model = xgboost.Booster(model_file = model_name)
#model=pickle.load(open(model_name , "rb"))

st.set_page_config(page_title='My Car Price 🚗', layout='wide')
home, price_estimator = st.tabs(["Home", "Price Estimator"])
with home:
	def get_base64(bin_file):
		with open(bin_file, 'rb') as f:
			data = f.read()
		return base64.b64encode(data).decode()

	def set_background(png_file):
        	bin_str = get_base64(png_file)
        	page_bg_img = '''
        	<style>
        	.stApp {
        	background-image: url("data:image/png;base64,%s");
        	background-size: cover;
        	}
        	</style>
        	''' % bin_str
        	st.markdown(page_bg_img, unsafe_allow_html=True)
	background_home = os.path.join(here, "Black Red Modern Car Maintenance Checklist Carousel Instagram Post.png")
	set_background(background_home)
	st.title('How Much is My Car Worth?')
	st.write("This website will give you an estimation of your car's price in the market.")
	with st.container():
		st.write("---")
		#left_column_h, right_column_h = st.columns(2)
		#with left_column_h:
			#*You can leave some options as the defualt value but it will affect the accuracy of the price estimation.*
		st.markdown(" ## What you need to do: ")
			#st.markdown("- ### Go to the *Price Estimator* tab.")
			#st.markdown("- ### Enter the requested information.")
			#st.markdown("- ### Press the *Predict* button.")
		st.write("""
- ### Go to the *Price Estimator* tab.
- ### Fill the *General Information* section or both *General Information* and *Extra Information* sections for more accurate estimation.
- ### Click the *Predict* button to get your car's price.

""") 
with price_estimator:

	car_models = ('Renault Megane', 'SEAT Leon', 'Volvo V40',
        	      'Dacia Sandero', 'Hyundai i30', 'Opel Astra', 'Ford Mustang',
        	      'Ford Mustang', 'Volvo C70', 'Peugeot 308', 'Ford Focus ', 'Nissan Qashqai',
                      'SEAT Ibiza', 'Fiat Tipo', 'Fiat', 'Renault Clio', 'Ford Fiesta', 'Nissan Micra', 'Fiat 500X',
          	      'Skoda Octavia', 'Volvo XC60', 'Opel Corsa', 'Dacia Duster', 'Toyota Yaris', 'Volvo V60',
                      'Opel Insignia', 'Peugeot 208', 'Skoda Fabia', 'Fiat 500C', 'Toyota Auris', 'Volvo C30',
                      'Peugeot RCZ', 'Hyundai TUCSON', 'Peugeot 3008', 'Ford Kuga', 'Volvo XC90', 'Volvo V90',
                      'Volvo XC40', 'Dacia Logan', 'Peugeot 508', 'Toyota Corolla', 'Skoda Scala', 'Skoda Superb',
                      'SEAT Ateca', 'SEAT Arona', 'Hyundai i20', 'Renault Captur', 'Ford Mondeo', 'Skoda Kodiaq',
                      'Nissan 370Z', 'Toyota C-HR', 'Skoda Karoq', 'Peugeot 2008', 'Renault Talisman', 'Peugeot 207',
                      'Opel Grandland X', 'Renault Kadjar', 'Toyota Aygo', 'Peugeot 206', 'Opel Cascada',
                      'Volvo S60', 'Mercedes-Benz A 180', 'Nissan X-Trail', 'Nissan 350Z', 'Volvo S90', 'Opel Adam',
                      'Nissan Pulsar', 'Fiat Panda', 'Toyota RAV 4', 'Hyundai IONIQ', 'Nissan Juke', 'Hyundai i10'
                      'Peugeot 307', 'Fiat 124 Spider', 'Renault Twingo', 'Opel Crossland X', 'Fiat 500L',
                      'Renault ZOE', 'Skoda Kamiq', 'Volvo V90 Cross Country', 'Renault Laguna', 'Dacia Jogger',
                      'Mercedes-Benz C 200', 'Mercedes-Benz A 200', 'Mercedes-Benz C 220', 'Toyota GT86',
                      'Toyota Land Cruiser', 'Other')
	with st.container():
		st.write("---")
		left_column, right_column = st.columns(2)
		with left_column:
			st.subheader("General Information")
			st.write("---")
			st.markdown("Choose your car model")
			car = st.selectbox('If there is no results of your car model, type "Other".', car_models)
			locations = ('Germany', 'Spain', 'Netherlands', 'Italy', 'Belgium',
                     		     'France', 'Austria', 'Luxembourg', 'Bulgaria', 'Other')
			st.write("##")
			st.markdown("Choose your location")			
			location = st.selectbox('If there is no results of your location, type "Other".', locations )
			body_types = ('Station wagon', 'Off-Road/Pick-up', 'Compact', 'Sedan', 'Coupe', 'Convertible')
			st.write("##")
			seller = st.radio("You are a:",("Dealer", "Private seller") )
			st.write("##")
			warranty= st.radio("Does your car have a warranty?",("Yes","No"))
			gearboxes = ('Manual', 'Automatic', 'Semi-automatic')
			gearbox= st.radio("Choose your car's gearbox",gearboxes )
			st.write("##")
			body_type= st.radio("Choose your car's body type", body_types )
			types = ('Used', 'Demonstration', 'Pre-registered', "Employee's car")
			st.write("##")
			typee= st.radio('Is your car', types )
			st.write("##")
			drivetrain = st.radio("Choose your car's drivetrain",("Front", "4WD", "Rear") )
			st.write("##")
			up_h = st.radio("Choose your car's upholestry",("Cloth",r"Part/Full Leather"))
			st.write("##")
			st.write("##")
			st.write("---")
			st.subheader("Extra Information")
			st.write("---")
			mileage= st.number_input("Insert your car's mileage", min_value=0.0)
			st.write("##")
			fuel_types = ('Benzine', 'Diesel', 'Electric', 'Liquid / Natural', 'Gas')
			st.write("##")
			fuel_type = st.radio("Choose your car's fuel",fuel_types )
			st.write("##")
			engine_s= st.number_input("Insert your car's engine size", min_value=0.0)
			st.write("##")
			gear= st.number_input("Insert your car's gears size", min_value=1.0)
			st.write("##")
			co_emm = st.number_input("Insert the CO2 emmision of your car", min_value=0.0)
			st.write("##")
			
			extras= st.number_input("How many extra features does your car have?", min_value=1.0)
			st.write("##")
			empty_w = st.number_input("Insert your car's empty weight in Kg", min_value=0.0)
			st.write("##")
			fsh = st.radio("Do you have your car's service history report?",("Yes","No"))
			st.write("##")
			
			pre_owner = st.number_input("How many previous owners did your car have?", min_value=1.0)
			st.write("##")
			energy = st.radio("How energy efficient is your car?",("efficient","unefficient"))
			st.write("##")
			age = st.number_input("Insert your car's age", min_value=0.0)
			power = st.number_input("Insert your car's power in kilowatt?", min_value=0.0)
			st.write("##")
			cons_avg = st.number_input("Choose your car's consumption average?", min_value=0.0)
			st.write("##")
			ccp = st.radio("Choose your car's comfort & convenience package?",("Standard","Premium", "Premium Plus"))
			st.write("##")
			emp = st.radio("Choose your car's entertainment & media package?",("Standard", "Plus"))
			st.write("##")
			ssp = st.radio("Choose your car's safety & security package?",("Safety Premium Package", "Safety Standard Package", "Safety Premium Plus Package"))
			obs = {'make_model':car, 'location':location, 'body_type': body_type, 'type': typee, 'warranty':warranty,
			       'mileage':mileage, 'gearbox': gearbox, 'fuel_type':fuel_type ,
			       'seller':seller, 'engine_size': engine_s,'gears':gear, 'co_emissions':co_emm,
			       'drivetrain':drivetrain, 'extras': extras, 'empty_weight':empty_w, 'full_service_history':fsh,
			       'upholstery':up_h, 'previous_owner':pre_owner, 'energy_efficiency_class': energy, 'age':age,
			       'power_kW':power, 'cons_avg':cons_avg, 'comfort_&_convenience_Package':ccp, 'entertainment_&_media_Package': emp,
			       'safety_&_security_Package': ssp}
			observation = pd.DataFrame([obs])
	with st.container():
		st.write("---")
		st.write("##")
		predict = st.button("Predict")
		st.markdown("""
<style>
.stButton>button {
  display: inline-block;
  padding: 15px 25px;
  font-size: 24px;
  cursor: pointer;
  text-align: center;
  text-decoration: none;
  outline: none;
  color: #fff;
  background-color: #D91A37;
  border: none;
  border-radius: 15px;
  box-shadow: 0 9px #999;
}

.stButton>button:hover {background-color: #EC1E3D}

.stButton>button:active {
  background-color: #9A1A2E;
  box-shadow: 0 5px #666;
  transform: translateY(4px);
}
</style>

""", unsafe_allow_html=True)
		result = model.predict(observation)
		resultf = round(result[0], 2)
		resultf = str(resultf)
		if predict and result>0:
			fs = 20
			message = "Your car's estimated price in the market is: "+resultf+" U.S dollars."
			html_str = f"""
<style>
p.a {{
  font: bold {fs}px Courier;
}}
</style>
<p class="a"; style="background-color:black;">{message}</p>
"""

			st.markdown(html_str, unsafe_allow_html=True)
		elif predict and result<=0:
			st.error('Please enter realistic values.')
#streamlit run C:\Users\fai-w\Desktop\streamlitDeployment\autoscoutStreamlit.py