#!/bin/bash

case "$1" in
  start)
    echo "Starting ChinaOrUS services..."
    docker-compose up -d
    ;;
  stop)
    echo "Stopping ChinaOrUS services..."
    docker-compose down
    ;;
  restart)
    echo "Restarting ChinaOrUS services..."
    docker-compose restart
    ;;
  logs)
    docker-compose logs -f
    ;;
  status)
    docker-compose ps
    ;;
  rebuild)
    echo "Rebuilding and restarting services..."
    docker-compose down
    docker-compose up -d --build
    ;;
  *)
    echo "Usage: $0 {start|stop|restart|logs|status|rebuild}"
    exit 1
    ;;
esac
