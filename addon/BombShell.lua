
local frame = CreateFrame("Frame", "MainFrame", UIParent)
frame:ClearAllPoints();
frame:SetHeight(300);
frame:SetWidth(300);
frame.text = frame:CreateFontString("Health", "BACKGROUND", "GameFontHighlightLarge")
frame.text:SetAllPoints()
frame.text:SetTextColor(0, 0, 0, 1)
frame:SetPoint("LEFT", 0, 200);
frame:SetBackdrop({bgFile = "Interface/AddOns/BombShell/data/b", 
edgeFile = "Interface/Tooltips/UI-Tooltip-Border", 
tile = true, tileSize = 16, edgeSize = 16, 
insets = { left = 4, right = 4, top = 4, bottom = 4 },
backdropColor = { r=1, g=1, b=1, a=0 }})
frame.texture = frame:CreateTexture(nil, "BACKGROUND")
frame.texture:SetAllPoints(true)
frame.texture:SetTexture(1, 1, 1, 1)
frame.text:SetText("HEALTH: " ..UnitHealth("player"))
frame:RegisterEvent("UNIT_HEALTH")
frame:SetScript('OnEvent', 
function (self)
    local health = UnitHealth("player")
    frame.text:SetText("HEALTH UPDATED: " ..health)
end)
function ShowFrame()
    frame:Show()
end
