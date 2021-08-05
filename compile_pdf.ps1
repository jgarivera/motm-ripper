$DefaultScratchpad = "scratchpad.md"
$DefaultOrg = "JISSA-APC"
$DefaultAgenda = "GeneralMeeting"

$BuildPath = "build"
    
If (!(test-path $BuildPath))
{
    md $BuildPath
}

if (!($ScratchPadName = Read-Host "Input scratchpad name ($($DefaultScratchpad))")) { $ScratchPadName = $DefaultScratchpad }
if (!($OrgName = Read-Host "Input organization name ($($DefaultOrg))")) { $OrgName = $DefaultOrg }
if (!($AgendaName = Read-Host "Input agenda name ($($DefaultAgenda))")) { $AgendaName = $DefaultAgenda }

$DateString = $(Get-Date).ToString('yyyyMMdd')
$FileName = "$($DateString)_$($OrgName)_$($AgendaName).pdf"

$HydratePath = "scratchpads/hydrated"
If (!(test-path $HydratePath)) { md $HydratePath }

Write-Host "Hydrating $($ScratchPadName)"

python parser.py $($ScratchPadName)

Write-Host "Writing to $($FileName)"

pandoc "scratchpads/hydrated/$ScratchPadName" -o "$BuildPath/$FileName" --template "templates/eisvogel.tex" --highlight-style tango --from markdown --listings