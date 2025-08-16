#!/bin/bash
# Health check script para Docker/Dokploy

# Verificar que la aplicación responde en el endpoint de health
curl -f http://localhost:8081/health || exit 1
