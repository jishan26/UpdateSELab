# Live Location Tracking System

A real-time location tracking system for the ambulance finder app that allows drivers to share their live locations and riders to see nearby drivers in real-time.

## 🚀 Features

- **Real-time Location Updates**: Drivers send their location every 5 seconds when logged in
- **Live Driver Tracking**: Riders see their own location plus all nearby drivers on a map
- **Multi-client Support**: Works across multiple devices (driver on one device, rider on another)
- **WebSocket Communication**: Fast, real-time communication between frontend and backend
- **Redux State Management**: Centralized state management for location data
- **Interactive Maps**: Beautiful, interactive maps with custom markers and tooltips

## 🏗️ Architecture

### Backend (FastAPI + WebSockets)

- **WebSocket Server**: Handles real-time connections and message routing
- **Driver Location Service**: Manages driver positions and nearby driver queries
- **Connection Manager**: Tracks active connections and user roles
- **Database Integration**: Stores driver locations in PostgreSQL

### Frontend (React + Redux)

- **LiveLocationMap Component**: Interactive map showing user and driver locations
- **WebSocket Handler**: Manages real-time communication
- **Redux Slices**: State management for user, driver locations, and nearby drivers
- **Dashboard Integration**: Seamlessly integrated into driver and rider dashboards

## 📁 File Structure

```
Backend/
├── FastAPI-demo/
│   ├── api.py                          # WebSocket endpoints and connection management
│   ├── driver_location_service.py      # Driver location management service
│   ├── models.py                       # Database models
│   └── requirements.txt                # Python dependencies

Frontend/
├── rapid_rescue/src/
│   ├── components/
│   │   ├── Map/
│   │   │   └── LiveLocationMap.jsx     # Main map component with driver markers
│   │   ├── DriverDashboard/
│   │   │   └── DriverDashboard.jsx     # Driver dashboard with location tracking
│   │   └── RiderDashboard/
│   │       └── RiderDashboard.jsx      # Rider dashboard with nearby drivers
│   ├── controllers/websocket/
│   │   └── handler.js                  # WebSocket message handling
│   └── store/slices/
│       ├── nearby-drivers-slice.js     # Redux slice for nearby drivers
│       └── user-slice.js               # Redux slice for user data
```

## 🔧 Setup Instructions

### Backend Setup

1. **Install Dependencies**

   ```bash
   cd FastAPI-demo
   pip install -r requirements.txt
   ```

2. **Start the Server**
   ```bash
   uvicorn api:app --reload --host 0.0.0.0 --port 8000
   ```

### Frontend Setup

1. **Install Dependencies**

   ```bash
   cd rapid_rescue
   npm install
   ```

2. **Start the Development Server**
   ```bash
   npm start
   ```

## 🎯 How It Works

### Driver Flow

1. Driver logs in and navigates to the driver dashboard
2. WebSocket connection is established with driver role
3. LiveLocationMap component starts periodic location tracking (every 5 seconds)
4. Location updates are sent to the backend via WebSocket
5. Backend stores location and broadcasts to all connected riders

### Rider Flow

1. Rider logs in and navigates to the rider dashboard
2. WebSocket connection is established with rider role
3. Rider receives current driver locations on connection
4. Rider's map shows their location plus all nearby drivers
5. Real-time updates show driver movements as they happen

## 📡 WebSocket Message Types

### Driver Messages

- `add-location`: Initial location update when driver comes online
- `update-location`: Periodic location updates (every 5 seconds)

### Backend Responses

- `location_updated`: Confirmation of location update
- `nearby-drivers`: Initial driver locations sent to riders
- `driver-location`: Real-time driver location updates sent to riders

## 🗺️ Map Features

### Driver Markers

- **Orange markers** with ambulance emoji (🚑)
- **Pulsing animation** to indicate live tracking
- **Tooltips** showing driver name, status, coordinates, and last update time
- **Real-time updates** as drivers move

### User Location

- **Green marker** for the current user
- **Accuracy circle** showing GPS accuracy
- **Live tracking indicator** in the info panel
- **Manual update button** for immediate location refresh

## 🔄 State Management

### Redux Slices

#### `nearbyDrivers`

```javascript
{
  drivers: {
    [driverId]: {
      latitude: number,
      longitude: number,
      timestamp: string,
      name: string,
      status: string
    }
  },
  lastUpdated: string,
  isTracking: boolean
}
```

#### `user`

```javascript
{
  id: number,
  name: string,
  email: string,
  role: string,
  latitude: number,
  longitude: number,
  token: string
}
```

## 🧪 Testing

Run the test script to simulate multiple drivers and riders:

```bash
python test_live_location.py
```

**Note**: You'll need valid JWT tokens from your authentication system for the test to work.

## 🚀 Usage Examples

### Driver Dashboard

```jsx
<LiveLocationMap
  height="420px"
  title="Your Live Location"
  trackPeriodically={true}
  updateInterval={5000}
  showAccuracy={true}
/>
```

### Rider Dashboard

```jsx
<LiveLocationMap
  height="100%"
  title="Your Location"
  trackPeriodically={false}
  showAccuracy={true}
  markerColor="#4CAF50"
  markerBorderColor="#2E7D32"
/>
```

## 🔧 Configuration

### Location Update Interval

- **Drivers**: 5 seconds (configurable via `updateInterval` prop)
- **Riders**: One-time location fetch (no periodic updates)

### Map Settings

- **Default Zoom**: 13
- **Tile Layer**: OpenStreetMap
- **Marker Colors**: Customizable via props
- **Accuracy Display**: Optional accuracy circles

## 🛡️ Security

- **JWT Authentication**: All WebSocket connections require valid tokens
- **Role-based Access**: Drivers and riders have different permissions
- **Input Validation**: All location data is validated before processing
- **Rate Limiting**: Built-in protection against spam updates

## 📊 Performance

- **Efficient Updates**: Only changed locations are broadcast
- **Memory Management**: Inactive drivers are automatically removed
- **Connection Cleanup**: Proper cleanup on disconnection
- **Optimized Rendering**: React components only re-render when necessary

## 🐛 Troubleshooting

### Common Issues

1. **No driver locations showing**

   - Check WebSocket connection status
   - Verify driver is logged in and sending updates
   - Check browser console for errors

2. **Location not updating**

   - Ensure location permissions are granted
   - Check if GPS is enabled
   - Verify network connection

3. **WebSocket connection failed**
   - Check if backend server is running
   - Verify CORS settings
   - Check authentication token validity

## 🔮 Future Enhancements

- **Geofencing**: Define service areas for drivers
- **Route Optimization**: Calculate optimal routes for drivers
- **Push Notifications**: Notify riders of nearby drivers
- **Analytics Dashboard**: Track driver performance and coverage
- **Offline Support**: Cache locations when offline
- **Real-time Chat**: Communication between drivers and riders

## 📝 License

This project is part of the Rapid Rescue ambulance finder application.
