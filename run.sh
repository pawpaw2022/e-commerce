#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}Starting E-commerce Application...${NC}"

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo -e "${RED}Python is not installed. Please install Python first.${NC}"
    exit 1
fi

# Check if required packages are installed
echo -e "${BLUE}Checking dependencies...${NC}"
if ! pip show fastapi streamlit &> /dev/null; then
    echo -e "${BLUE}Installing required packages...${NC}"
    pip install -r requirements.txt
fi

# Function to stop background processes on script exit
cleanup() {
    echo -e "\n${BLUE}Shutting down services...${NC}"
    kill $(jobs -p) 2>/dev/null
    exit 0
}

# Set up cleanup on script exit
trap cleanup EXIT

# Start FastAPI backend
echo -e "${GREEN}Starting FastAPI backend server...${NC}"
python -m app.main &
BACKEND_PID=$!

# Wait for backend to start
echo -e "${BLUE}Waiting for backend to start...${NC}"
sleep 3

# Check if backend is running
if ! kill -0 $BACKEND_PID 2>/dev/null; then
    echo -e "${RED}Failed to start backend server${NC}"
    exit 1
fi

# Start Streamlit frontend
echo -e "${GREEN}Starting Streamlit frontend...${NC}"
streamlit run streamlit_app.py &
FRONTEND_PID=$!

# Wait for frontend to start
echo -e "${BLUE}Waiting for frontend to start...${NC}"
sleep 3

# Check if frontend is running
if ! kill -0 $FRONTEND_PID 2>/dev/null; then
    echo -e "${RED}Failed to start frontend server${NC}"
    exit 1
fi

echo -e "${GREEN}Both servers are running!${NC}"
echo -e "${BLUE}Backend URL: http://localhost:8000${NC}"
echo -e "${BLUE}Frontend URL: http://localhost:8501${NC}"
echo -e "${BLUE}Press Ctrl+C to stop both servers${NC}"

# Wait for user interrupt
wait 