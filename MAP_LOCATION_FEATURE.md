# Map-Based Location Picker Feature

## Overview
This feature allows sellers to select property locations using an interactive map when listing properties. The implementation uses Leaflet.js with OpenStreetMap tiles.

## Features Implemented

### 1. Property Model Updates
- Added `latitude` and `longitude` fields to store property coordinates
- Fields are optional (null=True, blank=True) to maintain backward compatibility

### 2. Property Form Updates
- Added hidden input fields for latitude and longitude
- These fields are automatically populated by the map JavaScript

### 3. Interactive Map on Property Create/Edit Page
**Features:**
- Map centered on India (default) or user's current location
- Click anywhere on the map to place a marker
- Draggable marker for precise positioning
- Coordinates automatically saved to hidden form fields
- When editing, existing coordinates are displayed with a marker
- Responsive design with clear instructions

**User Flow:**
1. Seller opens "Add Property" or "Edit Property" page
2. Map appears with instructions
3. Seller clicks on map to mark location
4. Marker appears and can be dragged to adjust
5. Latitude and longitude are automatically captured
6. Form submission saves coordinates to database

### 4. Property Detail Page Map
**Features:**
- Displays property location on an interactive map
- Shows marker with property name and address in popup
- Centered on property coordinates with appropriate zoom level
- Falls back to info message if coordinates not available

## Technical Implementation

### Files Modified

1. **property/models.py**
   - Added latitude and longitude fields

2. **property/forms.py**
   - Added latitude and longitude to form fields
   - Set as HiddenInput widgets with specific IDs

3. **property/templates/property/property_form.html**
   - Added Leaflet CSS and JS
   - Added map container with styling
   - Added JavaScript for map initialization and interaction
   - Hidden fields render automatically but don't show in form layout

4. **property/templates/property/property_detail.html**
   - Added Leaflet CSS and JS
   - Added map container for displaying location
   - Added JavaScript to show property marker

5. **templates/base.html**
   - Added `{% block extra_css %}` for page-specific styles

### JavaScript Functionality

#### Property Form Map
```javascript
- Initialize map with Leaflet
- Add OpenStreetMap tile layer
- Handle map click events to place marker
- Make marker draggable
- Update hidden form fields on marker placement/drag
- Load existing coordinates when editing
- Optional: Get user's current location
```

#### Property Detail Map
```javascript
- Initialize map centered on property coordinates
- Add marker with popup showing property info
- Read-only view (no interaction needed)
```

## Usage

### For Sellers (Adding Property)
1. Navigate to "List Property"
2. Fill in property details
3. Scroll to "Property Location" section
4. Click on the map where your property is located
5. Drag the marker if you need to adjust the position
6. Complete the rest of the form and submit

### For Sellers (Editing Property)
1. Navigate to your dashboard
2. Click "Edit" on a property
3. The map will show the existing location marker
4. Click elsewhere or drag the marker to update location
5. Save changes

### For Buyers (Viewing Property)
1. Open any property detail page
2. Scroll to "Location" section
3. View the interactive map showing property location
4. Click on marker to see property name and address

## Database Migration

Migration created: `property/migrations/0002_property_latitude_property_longitude.py`

To apply:
```bash
python manage.py migrate property
```

## Dependencies

### External Libraries
- **Leaflet.js v1.9.4** - Interactive map library
- **OpenStreetMap** - Free map tiles

### CDN Links Used
```html
<!-- CSS -->
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />

<!-- JavaScript -->
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
```

## Configuration

### Default Map Settings
- **Initial Center:** India (20.5937°N, 78.9629°E)
- **Initial Zoom:** 5 (country view)
- **Property Detail Zoom:** 15 (street view)
- **Max Zoom:** 19

### Customization Options

To change default location, edit in `property_form.html`:
```javascript
var initialLat = existingLat || YOUR_LATITUDE;
var initialLng = existingLng || YOUR_LONGITUDE;
```

## Future Enhancements

Potential improvements:
1. **Geocoding Search** - Add search box to find locations by address
2. **Reverse Geocoding** - Auto-fill address fields based on marker position
3. **Multiple Markers** - Show nearby properties on detail page
4. **Custom Marker Icons** - Different icons for different property types
5. **Drawing Tools** - Allow sellers to draw property boundaries
6. **Satellite View** - Toggle between map and satellite imagery
7. **Distance Calculator** - Show distance to landmarks

## Browser Compatibility

Works on all modern browsers:
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Performance Notes

- Leaflet.js is lightweight (~40KB gzipped)
- OpenStreetMap tiles load on-demand
- No API keys required (free service)
- Maps are cached by browser

## Troubleshooting

### Map not displaying
- Check browser console for JavaScript errors
- Ensure Leaflet CSS and JS are loading
- Verify internet connection (for tile loading)

### Coordinates not saving
- Check that hidden input fields have correct IDs
- Verify form submission includes latitude/longitude
- Check browser console for JavaScript errors

### Existing location not showing
- Verify property has latitude and longitude values in database
- Check template is correctly passing coordinates to JavaScript

## Testing Checklist

- [ ] Map loads on property create page
- [ ] Can click map to place marker
- [ ] Marker is draggable
- [ ] Coordinates update in hidden fields
- [ ] Form submission saves coordinates
- [ ] Existing coordinates load when editing
- [ ] Property detail page shows map with marker
- [ ] Map works on mobile devices
- [ ] Works without coordinates (backward compatibility)

## Support

For issues or questions, refer to:
- Leaflet.js Documentation: https://leafletjs.com/
- OpenStreetMap: https://www.openstreetmap.org/
