pipeline {
    agent any

    triggers {
        pollSCM('H/5 * * * *')
    }

    environment {
        MYSQL_ROOT_PASSWORD = 'root_password_segura'
        MYSQL_DATABASE      = 'tienda_online'
        MYSQL_USER          = 'usuario_tienda'
        MYSQL_PASSWORD      = 'contraseña_segura_tienda'
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Obteniendo código del repositorio...'
            }
        }

        stage('Build') {
            steps {
                echo 'Construyendo la imagen de la aplicación web...'
                bat '"C:\\Users\\LENOVO\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin\\docker.exe" compose build'
            }
        }

        stage('Deploy & Test') {
            steps {
                echo 'Levantando los contenedores (web y db)...'
                bat '"C:\\Users\\LENOVO\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin\\docker.exe" compose up -d'
                
                echo 'Esperando a que la web responda (máximo 30 segundos)...'
                script {
                    def maxIntentos = 10
                    def exito = false
                    for (int i = 1; i <= maxIntentos; i++) {
                        try {
                            bat 'curl -f -s http://localhost:5000/productos'
                            echo "¡La web respondió en el intento ${i}!"
                            exito = true
                            break
                        } catch (Exception e) {
                            echo "Intento ${i} fallido. La web aún no responde. Esperando 3 segundos..."
                            bat 'powershell -Command "Start-Sleep -Seconds 3"'
                        }
                    }
                    if (!exito) {
                        error "La verificación de la web falló después de ${maxIntentos} intentos."
                    }
                }
                
                echo '¡Verificación exitosa! La web está en línea.'
            }
        }
    }

    post {
        always {
            echo 'Limpiando: Deteniendo y eliminando los contenedores...'
            bat '"C:\\Users\\LENOVO\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin\\docker.exe" compose down'
        }
    }
}