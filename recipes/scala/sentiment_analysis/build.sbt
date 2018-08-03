lazy val commonSettings  = Seq(
  name := "ml-sample-service",
  version := "0.0.2",
  organization :=  "com.adobe.platform.ml",
  scalaVersion := "2.11.8"
)

lazy val root = (project in file(".")).
  settings(commonSettings: _*).
  settings(
    libraryDependencies += "com.adobe.platform.ml" %% "authoring-sdk" % "0.2.1",
    libraryDependencies += "org.apache.spark" %% "spark-core" % "2.1.0" % "provided",
    libraryDependencies += "org.apache.spark" %% "spark-mllib" % "2.1.0" % "provided",
    libraryDependencies += "org.apache.spark" %% "spark-sql" % "2.1.0" % "provided",
    libraryDependencies += "com.databricks" %% "spark-csv" % "1.5.0" % "provided",
    libraryDependencies += "com.typesafe.scala-logging" % "scala-logging-slf4j_2.11" % "2.1.2"
  ).
  settings(
    artifact in (Compile, assembly) ~= { art =>
      art.copy(`classifier` = Some("assembly"))
    }
  ).
  settings(addArtifact(artifact in (Compile, assembly), assembly).settings: _*)

assemblyMergeStrategy in assembly := {
  case PathList("META-INF", xs @ _*) => MergeStrategy.discard
  case x => MergeStrategy.first
}

resolvers ++= Seq(
    "Artifactory" at "[[ARTIFACTORY URL]]"
  )

publishTo := Some("Artifactory Realm" at "[[ARTIFACT BASE URL]]")
credentials += Credentials("Artifactory Realm", "[[ARTIFACT HOST URL]]", System.getProperty("artifactoryUser"), System.getProperty("artifactoryToken"))
