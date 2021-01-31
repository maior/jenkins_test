node {
  stage('Parallel-test') {
      parallel 'Build-test-1' : {
          build job : 'Build-test-1'
      } , 'Build-test-2' : {
          build job : 'Build-test-2'
      } , 'Build-test-3' : {
          build job : 'Build-test-3'
      }
  }
}
pipeline {
    agent none 
    stages {
        stage('Build-test-4') {
            steps {
                build 'Build-test-4'
            }
        }
    }
}
