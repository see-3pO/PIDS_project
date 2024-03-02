from flask import request, render_template,jsonify
from flask import current_app as app

def update_location_arduino():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            latitude = data.get('latitude')
            longitude = data.get('longitude')
            print('Received latitude:', latitude)
            print('Received longitude:', longitude)
            app.logger.info('Data received successfully')
            return render_template('map.html', latitude=latitude, longitude=longitude)
            # return 'hello'
        else:
            return 'Content type is not supported'
      
    # elif request.method == 'GET':
    #     return 'Use POST method to update location'
    else:
        app.logger.error('Use POST method to update location')
        return 'Method not allowed'
