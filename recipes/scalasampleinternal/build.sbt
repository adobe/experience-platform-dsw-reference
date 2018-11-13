

lazy val commonSettings  = Seq(
  name := "ml-retail-sample-internal",
  version := "0.2.0",
  organization :=  "com.adobe.platform.ml",
  scalaVersion := "2.11.8"
)

lazy val root = (project in file(".")).
  settings(commonSettings: _*).
  settings(
    libraryDependencies += "com.adobe.platform.ml" % "authoring-sdk_2.11" % "0.14.0" classifier "jar-with-dependencies",
    libraryDependencies += "org.apache.spark" %% "spark-core" % "2.1.0",
    libraryDependencies += "org.apache.spark" %% "spark-mllib" % "2.1.0" ,
    libraryDependencies += "org.apache.spark" %% "spark-sql" % "2.1.0" ,
    libraryDependencies += "com.databricks" %% "spark-csv" % "1.5.0" ,
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
  "Artifactory" at "https://artifactory.corp.adobe.com/artifactory/maven-experienceplatform-release-local"
)


publishTo := Some("Artifactory Realm" at "https://artifactory.corp.adobe.com/artifactory/maven-experienceplatform-release/")
credentials += Credentials("Artifactory Realm", "artifactory.corp.adobe.com", "platci", "AKCp5Z2Y84JMqFMWY7dD3v71aLVSRTh7BW15A52CabCRTKkTxgRtAfDrCeVkvL5pbgiEB9P4S")
