local frame = CreateFrame("Frame", "MainFrame", UIParent)
frame:ClearAllPoints()
frame:SetHeight(600)
frame:SetWidth(320)

frame.text = frame:CreateFontString("Health", "BACKGROUND", "GameFontNormal")
frame.text:SetPoint("CENTER", 0, 0)
frame.text:SetJustifyH("LEFT")
frame.text:SetTextColor(0, 0, 0, 1)
frame.text:SetFont("Interface\\AddOns\\BombShell\\data\\font\\default.ttf", 24)

frame.mana = frame:CreateFontString("Mana", "BACKGROUND", "GameFontNormal")
frame.mana:SetPoint("CENTER", 0, -30)
frame.mana:SetJustifyH("LEFT")
frame.mana:SetTextColor(0, 0, 0, 1)
frame.mana:SetFont("Interface\\AddOns\\BombShell\\data\\font\\default.ttf", 24)

frame.posx = frame:CreateFontString("PositionY", "BACKGROUND", "GameFontNormal")
frame.posx:SetPoint("CENTER", 0, -60)
frame.posx:SetJustifyH("LEFT")
frame.posx:SetTextColor(0, 0, 0, 1)
frame.posx:SetFont("Interface\\AddOns\\BombShell\\data\\font\\default.ttf", 24)

frame.posy = frame:CreateFontString("PositionY", "BACKGROUND", "GameFontNormal")
frame.posy:SetPoint("CENTER", 0, -90)
frame.posy:SetJustifyH("LEFT")
frame.posy:SetTextColor(0, 0, 0, 1)
frame.posy:SetFont("Interface\\AddOns\\BombShell\\data\\font\\default.ttf", 24)

frame.combat = frame:CreateFontString("Combat", "BACKGROUND", "GameFontNormal")
frame.combat:SetPoint("CENTER", 0, -120)
frame.combat:SetJustifyH("LEFT")
frame.combat:SetTextColor(0, 0, 0, 1)
frame.combat:SetFont("Interface\\AddOns\\BombShell\\data\\font\\default.ttf", 24)

frame.targetHealth = frame:CreateFontString("TargetHealth", "BACKGROUND", "GameFontNormal")
frame.targetHealth:SetPoint("CENTER", 0, -150)
frame.targetHealth:SetJustifyH("LEFT")
frame.targetHealth:SetTextColor(0, 0, 0, 1)
frame.targetHealth:SetFont("Interface\\AddOns\\BombShell\\data\\font\\default.ttf", 24)

frame.facing = frame:CreateFontString("Facing", "BACKGROUND", "GameFontNormal")
frame.facing:SetPoint("CENTER", 0, -180)
frame.facing:SetJustifyH("LEFT")
frame.facing:SetTextColor(0, 0, 0, 1)
frame.facing:SetFont("Interface\\AddOns\\BombShell\\data\\font\\default.ttf", 24)

frame.distance = frame:CreateFontString("Distance", "BACKGROUND", "GameFontNormal")
frame.distance:SetPoint("CENTER", 0, -210)
frame.distance:SetJustifyH("LEFT")
frame.distance:SetTextColor(0, 0, 0, 1)
frame.distance:SetFont("Interface\\AddOns\\BombShell\\data\\font\\default.ttf", 24)

frame.ability = frame:CreateFontString("Distance", "BACKGROUND", "GameFontNormal")
frame.ability:SetPoint("CENTER", 0, -240)
frame.ability:SetJustifyH("LEFT")
frame.ability:SetTextColor(0, 0, 0, 1)
frame.ability:SetFont("Interface\\AddOns\\BombShell\\data\\font\\default.ttf", 24)

--frame.tuid = frame:CreateFontString("Target ID", "BACKGROUND", "GameFontNormal")
--frame.tuid:SetPoint("CENTER", 0, -270)
--frame.tuid:SetJustifyH("LEFT")
--frame.tuid:SetTextColor(0, 0, 0, 1)
--frame.tuid:SetFont("Interface\\AddOns\\BombShell\\data\\font\\default.ttf", 24)

frame:SetPoint("LEFT", 0, 200)

frame:SetBackdrop(
    {
        insets = {left = 4, right = 4, top = 4, bottom = 4},
        backdropColor = {r = 1, g = 1, b = 1, a = 0}
    }
)
frame.texture = frame:CreateTexture(nil, "BACKGROUND")
frame.texture:SetAllPoints(true)
frame.texture:SetTexture(1, 1, 1, 1)
frame.text:SetText("HEALTH: " .. UnitHealth("player"))
frame.mana:SetText("MANA: " .. UnitHealth("player"))

frame:RegisterEvent("UNIT_HEALTH")
frame:RegisterEvent("UNIT_MANA")
frame:RegisterEvent("PLAYER_ENTERING_WORLD")
frame:RegisterEvent("PLAYER_REGEN_DISABLED")
frame:RegisterEvent("PLAYER_REGEN_ENABLED")
frame:RegisterEvent("PLAYER_TARGET_CHANGED")
frame:RegisterEvent("COMBAT_LOG_EVENT_UNFILTERED")
frame:SetScript(
    "OnEvent",
    function(...)
        if (event == "PLAYER_ENTERING_WORLD") then
            SetMapToCurrentZone()
            DEFAULT_CHAT_FRAME:AddMessage("ENTER WORLD")
            frame.combat:SetText("COMBAT: 0")
            frame.distance:SetText("TDIST: " .. -1)
            frame.targetHealth:SetText("THP: " .. -1)
--            frame.tuid:SetText("TID: " .. 0)
            frame.ability:SetText("SPELL: " .. -1)
        elseif (event == "UNIT_HEALTH") then
            local health = UnitHealth("player")
            local targetHealth = UnitHealth("target")
            frame.text:SetText("HEALTH: " .. health)
            frame.targetHealth:SetText("THP: " .. targetHealth)
        elseif (event == "UNIT_MANA") then
            local mana = UnitMana("player")
            frame.mana:SetText("MANA: " .. mana)
        elseif (event == "PLAYER_REGEN_ENABLED") then
            frame.combat:SetText("COMBAT: 0")
        elseif (event == "PLAYER_REGEN_DISABLED") then
            frame.combat:SetText("COMBAT: 1")
        elseif (event == "PLAYER_TARGET_CHANGED") then
            local tuid = UnitLevel("target")
            local targetHealth = UnitHealth("target")
            local max_health = UnitHealthMax("target");
            if (max_health == 0) then
                targetHealth = -1
            end
            local distance = 0
            if (CheckInteractDistance("target", 3)) then
                distance = 1
            elseif (CheckInteractDistance("target", 4)) then
                distance = 2
            end
            frame.distance:SetText("TDIST: " .. distance)
            frame.targetHealth:SetText("THP: " .. targetHealth)
--            frame.tuid:SetText("TID: " .. tuid)
        elseif (event == "COMBAT_LOG_EVENT_UNFILTERED") then
           local timestamp, subevent, _ = CombatLogGetCurrentEventInfo()
            DEFAULT_CHAT_FRAME:AddMessage("COMBAT LOG " .. subevent .. timestamp)
            if (subevent == "SPELL_FAILED_TOO_CLOSE") then
                frame.ability:SetText("SPELL: " .. 3)
            elseif (subevent == "SPELL_FAILED_LINE_OF_SIGHT") then
                frame.ability:SetText("SPELL: " .. 2)
            elseif (subevent == "SPELL_FAILED_OUT_OF_RANGE") then
                frame.ability:SetText("SPELL: " .. 1)
            elseif (subevent == "SPELL_FAILED_NOT_BEHIND") then
                frame.ability:SetText("SPELL: " .. 4)
            elseif (subevent == "SPELL_FAILED_UNIT_NOT_INFRONT") then
                frame.ability:SetText("SPELL: " .. 5)
            elseif (subevent == "SPELL_FAILED_BAD_IMPLICIT_TARGETS") then
                frame.ability:SetText("SPELL: " .. 6)
            end
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
