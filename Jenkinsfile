pipeline {
    agent any

    triggers {
        pollSCM('H/5 * * * *')
    }

    environment {
    // Añadimos la carpeta de Docker al PATH para que encuentre el credential helper
    PATH = "C:\\Users\\LENOVO\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin;${env.PATH}"
    
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
                // Usando la ruta exacta de tu usuario LENOVO
                bat '"C:\\Users\\LENOVO\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin\\docker.exe" compose build'
            }
        }

        stage('Deploy & Test') {
            steps {
                echo 'Levantando los contenedores (web y db)...'
                bat '"C:\\Users\\LENOVO\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin\\docker.exe" compose up -d'
                
                echo 'Esperando a que la base de datos y la web estén listas...'
                bat 'timeout /t 20 /nobreak'
                
                echo 'Ejecutando operación de ejemplo: Verificando que la web responda...'
                bat 'curl -f http://localhost:5000/productos || exit 1'
                
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