lazy val commonSettings  = Seq(
  name := "ml-sample-service",
  version := "0.0.1",
  organization :=  "com.adobe.platform.ml",
  scalaVersion := "2.11.8"
)

lazy val root = (project in file(".")).
  settings(commonSettings: _*).
  settings(
    libraryDependencies += "com.adobe.platform.ml.algorithm" %% "xgboost4j" % "0.7" % "provided" classifier "linux",
    libraryDependencies += "com.adobe.platform.ml.algorithm" %% "xgboost4j-spark" % "0.7" % "provided" classifier "linux",
    libraryDependencies += "com.adobe.platform.ml" %% "authoring-sdk" % "0.0.4",
    libraryDependencies += "org.apache.spark" %% "spark-core" % "2.1.0" % "provided",
    libraryDependencies += "org.apache.spark" %% "spark-mllib" % "2.1.0" % "provided",
    libraryDependencies += "org.apache.spark" %% "spark-sql" % "2.1.0" % "provided",
    libraryDependencies += "com.databricks" %% "spark-csv" % "1.5.0" % "provided",
    libraryDependencies += "com.typesafe.scala-logging" % "scala-logging-slf4j_2.11" % "2.1.2" % "provided"

  )

resolvers ++= Seq(
  "Artifactory" at "[[ARTIFACTORY URL]]/maven-experienceplatform-release-local"
)