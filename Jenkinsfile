pipeline {
    agent any

    triggers {
        // Poll SCM: Jenkins revisará GitHub cada 5 minutos en busca de cambios
        pollSCM('H/5 * * * *')
    }

    environment {
        
         // Añadimos la ruta de Docker al PATH de Jenkins
    PATH = "C:\\Program Files\\Docker\\Docker\\resources\\bin;${env.PATH}"

        // Variables para que docker-compose cree la base de datos
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
                // Usamos bat porque Jenkins está en Windows
                bat 'docker compose build'
            }
        }

        stage('Deploy & Test') {
            steps {
                echo 'Levantando los contenedores (web y db)...'
                bat 'docker compose up -d'
                
                echo 'Esperando a que la base de datos y la web estén listas...'
                // Pausa de 20 segundos
                bat 'timeout /t 20 /nobreak'
                
                echo 'Ejecutando operación de ejemplo: Verificando que la web responda...'
                // Si la web falla o no responde, curl devuelve error y el pipeline falla
                bat 'curl -f http://localhost:5000/productos || exit 1'
                
                echo '¡Verificación exitosa! La web está en línea.'
            }
        }
    }

    post {
        always {
            echo 'Limpiando: Deteniendo y eliminando los contenedores...'
            // Se ejecuta SIEMPRE, incluso si falla el paso anterior
            bat 'docker compose down'
        }
    }
}