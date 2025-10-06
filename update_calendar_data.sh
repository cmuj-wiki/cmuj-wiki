#!/bin/bash
#
# Master Build Script - Calendar Data Pipeline
# ============================================
#
# This script regenerates all calendar JSON data from source files.
# Run this whenever the XLSX or PDF calendar files are updated.
#
# Usage: ./update_calendar_data.sh
#

set -e  # Exit on any error

echo "🔄 CMUJ Wiki - Calendar Data Update"
echo "===================================="
echo ""

# Check if source files exist
if [ ! -f "I-rok-2024-2025_www_zimowy.xlsx" ]; then
    echo "❌ Error: I-rok-2024-2025_www_zimowy.xlsx not found"
    exit 1
fi

# Step 1: Parse schedule from XLSX
echo "📚 Step 1/2: Parsing schedule from XLSX..."
python3 parse_schedule_v2.py
if [ $? -ne 0 ]; then
    echo "❌ Error: Schedule parsing failed"
    exit 1
fi
echo "✅ Schedule data generated"
echo ""

# Step 2: Parse academic calendar (holidays, exam sessions)
echo "📅 Step 2/2: Parsing academic calendar..."
python3 calendar_parser.py
if [ $? -ne 0 ]; then
    echo "❌ Error: Calendar parsing failed"
    exit 1
fi
echo "✅ Academic calendar data generated"
echo ""

# Validate output files exist
echo "🔍 Validating output files..."
if [ ! -f "docs/static/schedule_data_v2.json" ]; then
    echo "❌ Error: schedule_data_v2.json not generated"
    exit 1
fi

if [ ! -f "docs/static/holidays.json" ]; then
    echo "❌ Error: holidays.json not generated"
    exit 1
fi

# Basic JSON validation
echo "🔍 Validating JSON format..."
python3 -m json.tool docs/static/schedule_data_v2.json > /dev/null
if [ $? -ne 0 ]; then
    echo "❌ Error: schedule_data_v2.json is not valid JSON"
    exit 1
fi

python3 -m json.tool docs/static/holidays.json > /dev/null
if [ $? -ne 0 ]; then
    echo "❌ Error: holidays.json is not valid JSON"
    exit 1
fi

echo "✅ JSON files validated"
echo ""

# Show summary
echo "📊 Summary:"
SCHEDULE_EVENTS=$(python3 -c "import json; print(len(json.load(open('docs/static/schedule_data_v2.json'))))")
HOLIDAY_EVENTS=$(python3 -c "import json; print(len(json.load(open('docs/static/holidays.json'))))")

echo "  - schedule_data_v2.json: ${SCHEDULE_EVENTS} events"
echo "  - holidays.json: ${HOLIDAY_EVENTS} events"
echo ""

echo "🎉 Calendar data update complete!"
echo ""
echo "💡 Next steps:"
echo "   1. Test the calendar widget at docs/kalendarz/index.md"
echo "   2. Commit the updated JSON files if everything looks good"
echo "   3. Deploy to production"
