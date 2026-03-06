# Location Search Feature Guide

## Overview
The location search feature allows sellers to quickly find and mark property locations by searching for addresses, cities, or landmarks instead of manually navigating the map.

## How to Use

### Method 1: Search by Address/Location

1. **Enter Search Query**
   - Type in the search box: address, city, landmark, or place name
   - Examples:
     - "Connaught Place, New Delhi"
     - "Mumbai Central Station"
     - "Bangalore, Karnataka"
     - "Taj Mahal, Agra"
     - "MG Road, Pune"

2. **Execute Search**
   - Press Enter key, OR
   - Click the "Search" button

3. **View Results**
   - Up to 5 matching locations will appear below the search box
   - Each result shows the full address/location name

4. **Select Location**
   - Click on any search result
   - Map automatically zooms to that location
   - Marker is placed at the selected coordinates
   - Search box is populated with the selected location name

5. **Fine-tune Position**
   - Drag the marker to adjust exact position if needed
   - Or click elsewhere on the map to reposition

### Method 2: Direct Map Click

1. **Navigate Map**
   - Use mouse to pan and zoom the map
   - Scroll to zoom in/out
   - Drag to move around

2. **Click to Mark**
   - Click anywhere on the map
   - Marker appears at clicked location

3. **Adjust Position**
   - Drag marker to fine-tune position

## Search Tips

### Be Specific
- ✅ Good: "Connaught Place, New Delhi"
- ❌ Too vague: "Delhi"

### Include City/State
- ✅ Good: "MG Road, Bangalore"
- ⚠️ Less accurate: "MG Road" (many cities have MG Road)

### Use Landmarks
- ✅ Good: "Near Gateway of India, Mumbai"
- ✅ Good: "Opposite Phoenix Mall, Chennai"

### Try Different Formats
If first search doesn't work, try:
- Full address: "123 Main Street, Sector 5, Gurgaon, Haryana"
- Landmark + City: "India Gate, New Delhi"
- Area + City: "Bandra West, Mumbai"
- Pincode: "110001, Delhi"

## Search Results

### Understanding Results
Each result shows:
- **Full location name** - Complete address or place description
- Results are ordered by relevance

### No Results Found?
If search returns no results:
1. Check spelling
2. Try a broader search (e.g., just city name)
3. Use the map click method instead
4. Try searching for a nearby landmark

### Multiple Results
If you see multiple similar results:
- Read the full address carefully
- Look for the one that matches your property location
- Click on the most accurate result
- You can always adjust the marker position after

## Technical Details

### Geocoding Service
- Uses **Nominatim** (OpenStreetMap's geocoding API)
- Free service, no API key required
- Searches worldwide locations
- Returns latitude and longitude coordinates

### Rate Limits
- Maximum 1 search per second
- For normal usage, this is sufficient
- If you need to search multiple times, wait 1-2 seconds between searches

### Data Source
- Based on OpenStreetMap data
- Community-maintained
- Generally accurate for major locations
- May have limited data for very remote areas

## Examples

### Example 1: Residential Property in Delhi
```
Search: "Vasant Vihar, New Delhi"
Results:
1. Vasant Vihar, New Delhi, Delhi, 110057, India
2. Vasant Vihar Metro Station, New Delhi, India
3. Vasant Vihar Market, New Delhi, India

Action: Click on result #1
Result: Map zooms to Vasant Vihar area, marker placed
```

### Example 2: Commercial Property in Mumbai
```
Search: "Nariman Point, Mumbai"
Results:
1. Nariman Point, Mumbai, Maharashtra, 400021, India
2. Nariman Point Bus Station, Mumbai, India

Action: Click on result #1
Result: Map shows Nariman Point business district
```

### Example 3: Property Near Landmark
```
Search: "Near Indiranagar Metro, Bangalore"
Results:
1. Indiranagar Metro Station, Bangalore, Karnataka, India
2. Indiranagar, Bangalore, Karnataka, 560038, India

Action: Click on result #2 for the area, or #1 for the metro station
Result: Map centers on Indiranagar
Then: Drag marker to exact property location
```

## Troubleshooting

### Search Button Not Working
- Check internet connection
- Ensure search box has text
- Try pressing Enter instead of clicking button

### Results Not Appearing
- Wait 1-2 seconds after previous search
- Check browser console for errors
- Try a different search term

### Wrong Location Selected
- Click on a different search result
- Or click directly on the map at correct location
- Drag marker to adjust position

### Search Too Slow
- Nominatim API may be experiencing high traffic
- Try again after a few seconds
- Use map click method as alternative

## Best Practices

### For Accurate Results
1. Start with a broad search (city/area)
2. Then refine by dragging marker
3. Use landmarks for reference
4. Verify location on map before submitting

### For Faster Workflow
1. If you know approximate location, zoom to that area first
2. Then use search to find exact address
3. Or just click on map if you can see the location

### For Remote Areas
1. Search for nearest town/city
2. Then navigate map manually
3. Click to place marker at property location

## Privacy & Data

### What Gets Saved
- Only latitude and longitude coordinates
- No search queries are stored
- No personal location data is tracked

### What Gets Sent to Nominatim
- Your search query
- User-Agent header (identifies the application)
- No personal information

## Support

For issues with:
- **Search functionality**: Check browser console for errors
- **Map not loading**: Verify internet connection
- **Inaccurate results**: Try different search terms or use map click
- **API errors**: Wait a few seconds and try again

## Additional Resources

- OpenStreetMap: https://www.openstreetmap.org/
- Nominatim Documentation: https://nominatim.org/
- Leaflet.js Documentation: https://leafletjs.com/
