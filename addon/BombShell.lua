local frame = CreateFrame("Frame", "MainFrame", UIParent)
frame:ClearAllPoints()
frame:SetHeight(600)
frame:SetWidth(300)

frame.text = frame:CreateFontString("Health", "BACKGROUND", "GameFontNormal")
frame.text:SetPoint("CENTER", 0, 0)
frame.text:SetJustifyH("LEFT")
frame.text:SetTextColor(0, 0, 0, 1)
frame.text:SetFont("Interface\\AddOns\\BombShell\\data\\font\\default.ttf", 22)

frame.mana = frame:CreateFontString("Mana", "BACKGROUND", "GameFontNormal")
frame.mana:SetPoint("CENTER", 0, -30)
frame.mana:SetJustifyH("LEFT")
frame.mana:SetTextColor(0, 0, 0, 1)
frame.mana:SetFont("Interface\\AddOns\\BombShell\\data\\font\\default.ttf", 22)

frame.posx = frame:CreateFontString("PositionY", "BACKGROUND", "GameFontNormal")
frame.posx:SetPoint("CENTER", 0, -60)
frame.posx:SetJustifyH("LEFT")
frame.posx:SetTextColor(0, 0, 0, 1)
frame.posx:SetFont("Interface\\AddOns\\BombShell\\data\\font\\default.ttf", 22)

frame.posy = frame:CreateFontString("PositionY", "BACKGROUND", "GameFontNormal")
frame.posy:SetPoint("CENTER", 0, -90)
frame.posy:SetJustifyH("LEFT")
frame.posy:SetTextColor(0, 0, 0, 1)
frame.posy:SetFont("Interface\\AddOns\\BombShell\\data\\font\\default.ttf", 22)

frame.combat = frame:CreateFontString("Combat", "BACKGROUND", "GameFontNormal")
frame.combat:SetPoint("CENTER", 0, -120)
frame.combat:SetJustifyH("LEFT")
frame.combat:SetTextColor(0, 0, 0, 1)
frame.combat:SetFont("Interface\\AddOns\\BombShell\\data\\font\\default.ttf", 22)

frame.targetHealth = frame:CreateFontString("TargetHealth", "BACKGROUND", "GameFontNormal")
frame.targetHealth:SetPoint("CENTER", 0, -150)
frame.targetHealth:SetJustifyH("LEFT")
frame.targetHealth:SetTextColor(0, 0, 0, 1)
frame.targetHealth:SetFont("Interface\\AddOns\\BombShell\\data\\font\\default.ttf", 22)

frame.facing = frame:CreateFontString("Facing", "BACKGROUND", "GameFontNormal")
frame.facing:SetPoint("CENTER", 0, -180)
frame.facing:SetJustifyH("LEFT")
frame.facing:SetTextColor(0, 0, 0, 1)
frame.facing:SetFont("Interface\\AddOns\\BombShell\\data\\font\\default.ttf", 22)

frame.distance = frame:CreateFontString("Facing", "BACKGROUND", "GameFontNormal")
frame.distance:SetPoint("CENTER", 0, -210)
frame.distance:SetJustifyH("LEFT")
frame.distance:SetTextColor(0, 0, 0, 1)
frame.distance:SetFont("Interface\\AddOns\\BombShell\\data\\font\\default.ttf", 22)

frame:SetPoint("LEFT", 0, 200)

frame:SetBackdrop(
    {
        bgFile = "Interface/AddOns/BombShell/data/b",
        edgeFile = "Interface/Tooltips/UI-Tooltip-Border",
        tile = true,
        tileSize = 16,
        edgeSize = 16,
        insets = {left = 4, right = 4, top = 4, bottom = 4},
        backdropColor = {r = 1, g = 1, b = 1, a = 0}
    }
)
frame.texture = frame:CreateTexture(nil, "BACKGROUND")
frame.texture:SetAllPoints(true)
frame.texture:SetTexture(1, 1, 1, 1)

frame.text:SetText("HEALTH: " .. UnitHealth("player"))

frame:RegisterEvent("UNIT_HEALTH")
frame:RegisterEvent("UNIT_MANA")
frame:RegisterEvent("PLAYER_ENTERING_WORLD")
frame:RegisterEvent("PLAYER_REGEN_DISABLED")
frame:RegisterEvent("PLAYER_REGEN_ENABLED")
frame:RegisterEvent("PLAYER_TARGET_CHANGED")
frame:SetScript(
    "OnEvent",
    function(...)
        if (event == "PLAYER_ENTERING_WORLD") then
            SetMapToCurrentZone()
            DEFAULT_CHAT_FRAME:AddMessage("ENTER WORLD")
        elseif (event == "UNIT_HEALTH") then
            local health = UnitHealth("player")
            local targetHealth = UnitHealth("target")
            frame.text:SetText("HEALTH: " .. health)
            frame.targetHealth:SetText("TARGET HEALTH: " .. targetHealth)
        elseif (event == "UNIT_MANA") then
            local mana = UnitMana("player")
            frame.mana:SetText("MANA: " .. mana)
        elseif (event == "PLAYER_REGEN_ENABLED") then
            frame.combat:SetText("COMBAT: 0")
        elseif (event == "PLAYER_REGEN_DISABLED") then
            frame.combat:SetText("COMBAT: 1")
        elseif (event == "PLAYER_TARGET_CHANGED") then
            local distance = 0
            if (CheckInteractDistance("target", 3)) then
                distance = 1
            elseif (CheckInteractDistance("target", 4)) then
                distance = 2
            end
            frame.distance:SetText("TARGET DISTANCE: " .. distance)
        end
    end
)

function GetPlayerFacing()
    local p = Minimap
    local m = ({p:GetChildren()})[9]
    return m:GetFacing()
end

function GetTruePosition()
    local posX, posY = GetPlayerMapPosition("player")
    local w = WorldMapButton:GetWidth()
    local h = WorldMapButton:GetHeight()
    return posX * w, posY * h
end

frame:SetScript(
    "OnUpdate",
    function(self, event)
        local posX, posY = GetTruePosition()
        frame.posx:SetText("X: " .. string.sub(posX, 0, 8))
        frame.posy:SetText("Y: " .. string.sub(posY, 0, 8))

        frame.facing:SetText("FACING: " .. string.sub(GetPlayerFacing(), 0, 8))
    end
)
function ShowFrame()
    frame:Show()
end
