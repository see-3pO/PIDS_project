import winsdk.windows.devices.geolocation as wdg, asyncio
async def getCoords():
        locator = wdg.Geolocator()
        pos = await locator.get_geoposition_async()
        print(pos.coordinate.latitude, pos.coordinate.longitude)
        pos_latitude = pos.coordinate.latitude
        pos_longitude = pos.coordinate.longitude
        return pos_latitude, pos_longitude
    
def getLoc():
    return asyncio.run(getCoords())