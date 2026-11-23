pipeline {
    agent any

    triggers {
        pollSCM('H/5 * * * *')
    }

    environment {
        // 1. Añadimos la ruta de Docker al PATH de Jenkins (¡Clave para las credenciales!)
        PATH = "C:\\Users\\LENOVO\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin;${env.PATH}"
        
        // 2. Variables de la base de datos
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
                // Usamos la ruta absoluta de docker
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
                            // Usamos ruta absoluta para curl
                            bat '"C:\\Windows\\System32\\curl.exe" -f -s http://localhost:5000/productos'
                            echo "¡La web respondió en el intento ${i}!"
                            exito = true
                            break
                        } catch (Exception e) {
                            echo "Intento ${i} fallido. La web aún no responde. Esperando 3 segundos..."
                            // Usamos ruta absoluta para PowerShell
                            bat '"C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command "Start-Sleep -Seconds 3"'
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