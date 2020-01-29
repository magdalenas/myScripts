Write-Host $args

$env = $args | Get-Random # in case next one doesn't work

try {
  $baseUrl = "http://some.url/buildlocks"
  $health = "/healthz/live"
  $poolName = "end2endtest"
  $envs = $args
  # check if service works fine
  $res = Invoke-WebRequest -Uri "$baseUrl$health"
  if ($res.StatusCode -ne 200) {
    throw "BuildLock service is not available"
  }
  $concurrentBuilds = 0
  foreach ($arg in $args) {
    $res = Invoke-RestMethod -Uri "$baseUrl/$poolName/$arg"
    if ($res.status -eq "available") {
      Write-Host "<$arg> was avaialable"
      $env = $arg
      break
    }
    $envBuilds = ($res.content | Get-Unique | Measure-Object -line).Lines
    Write-host "EnvBuilds: $envBuilds for $arg"
    Write-Host "Concurrent builds: $concurrentBuilds"
    if ($concurrentBuilds -eq 0 -or $concurrentBuilds -ge $envBuilds) {
      $concurrentBuilds = $envBuilds
      Write-Host "Picked $arg"
      $env = $arg
    }
  }
}
catch {
  Write-Host "Something went wrong with request to locks. Will use the regular random thingy"
  Write-Host $PSItem.ToString()
}

Write-Host "Selected: $env"
Write-Host "##teamcity[setParameter name='Lock.Environment' value='$env']"
