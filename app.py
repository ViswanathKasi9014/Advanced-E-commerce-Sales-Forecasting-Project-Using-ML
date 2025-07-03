from flask import Flask, render_template, request
import joblib  # For loading the saved model
import os

app = Flask(__name__)

# Load the model once when the server starts to avoid reloading it on every request
try:
    model_path = os.path.join("Models", "decision.joblib")
    model = joblib.load(model_path)
    print("Model loaded successfully.")
except Exception as e:
    model = None
    print(f"Failed to load model: {e}")

@app.route("/", methods=["GET", "POST"])
def prediction():
    if request.method == "POST":
        try:
            # Retrieve and validate input values
            ShipYear = int(request.form['ShipYear'])
            OrderMonth = int(request.form['OrderMonth'])
            DayOfWeek = int(request.form['DayOfWeek'])

            # Prepare input for the model
            new_values = [[ShipYear, OrderMonth, DayOfWeek]]

            # Ensure model is loaded properly
            if model is None:
                raise ValueError("Model is not loaded properly. Please check the server logs.")

            # Make a prediction
            pred = model.predict(new_values)
            prediction_result = f"The prediction is: {pred[0]}"
            return render_template("prediction.html", results=prediction_result)

        except ValueError as ve:
            return render_template("prediction.html", results=f"Invalid input: {ve}")
        except Exception as e:
            return render_template("prediction.html", results=f"Error during prediction: {e}")

    return render_template("prediction.html", results=None)

if __name__ == "__main__":
    app.run(debug=True)
