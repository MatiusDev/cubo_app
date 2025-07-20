#!/usr/bin/env python3
"""
Script de prueba para verificar que la aplicación funciona correctamente
"""
import requests
import time
import subprocess
import sys
import threading
from pathlib import Path

def test_backend():
    """Prueba el backend directamente"""
    print("🧪 Probando backend...")
    
    try:
        # Importar y probar la aplicación
        sys.path.append(str(Path(__file__).parent / "backend"))
        from app.main import app
        
        # Crear un cliente de prueba
        from fastapi.testclient import TestClient
        client = TestClient(app)
        
        # Probar endpoint raíz
        response = client.get("/")
        assert response.status_code == 200
        assert "Hello" in response.json()
        print("✅ Endpoint / funciona correctamente")
        
        # Probar endpoint items
        response = client.get("/items")
        assert response.status_code == 200
        assert "values" in response.json()
        print("✅ Endpoint /items funciona correctamente")
        
        return True
        
    except Exception as e:
        print(f"❌ Error probando backend: {e}")
        return False

def test_server():
    """Prueba el servidor completo"""
    print("🧪 Probando servidor completo...")
    
    try:
        # Iniciar el servidor en un hilo
        server_process = None
        
        def start_server():
            nonlocal server_process
            backend_dir = Path(__file__).parent / "backend"
            server_script = backend_dir / "app" / "server.py"
            server_process = subprocess.Popen([
                sys.executable, str(server_script)
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Iniciar servidor
        server_thread = threading.Thread(target=start_server)
        server_thread.daemon = True
        server_thread.start()
        
        # Esperar a que el servidor inicie
        time.sleep(5)
        
        # Probar endpoints
        try:
            response = requests.get("http://localhost:8000/", timeout=10)
            assert response.status_code == 200
            print("✅ Servidor responde correctamente")
            
            response = requests.get("http://localhost:8000/items", timeout=10)
            assert response.status_code == 200
            print("✅ API funciona correctamente")
            
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Error conectando al servidor: {e}")
            return False
            
        finally:
            # Detener servidor
            if server_process:
                server_process.terminate()
                server_process.wait()
    
    except Exception as e:
        print(f"❌ Error probando servidor: {e}")
        return False

def main():
    """Función principal de pruebas"""
    print("🚀 Iniciando pruebas de Cubo App...")
    print()
    
    # Probar backend
    backend_ok = test_backend()
    print()
    
    # Probar servidor completo
    server_ok = test_server()
    print()
    
    # Resultados
    if backend_ok and server_ok:
        print("🎉 ¡Todas las pruebas pasaron!")
        print("✅ La aplicación está lista para usar")
    else:
        print("❌ Algunas pruebas fallaron")
        print("💡 Revisa los errores anteriores")
        sys.exit(1)

if __name__ == "__main__":
    main() 