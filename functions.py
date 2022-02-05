class taint:
  def colour(measurement_incidence, colours):
    if int(measurement_incidence) < 50:
      return colours.get("Lime")
    elif int(measurement_incidence) in range(50,200):
      return colours.get("Green")
    elif int(measurement_incidence) in range(200,400):
      return colours.get("Yellow")
    elif int(measurement_incidence) in range(400,600):
      return colours.get("Orange")
    elif int(measurement_incidence) in range(600, 800):
       return colours.get("Red")
    elif int(measurement_incidence) > 800:
      return colours.get("Black")
