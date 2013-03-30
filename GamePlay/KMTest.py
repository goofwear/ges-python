from DeathMatch import DeathMatch
import GEPlayer, GEUtil, GEGlobal as Glb, GEMPGameRules as GERules
from GEUtil import TempEnt as TE, Color, TraceOpt
from .Utils import GetPlayers

USING_API = Glb.API_VERSION_1_0_0

class KMTest( DeathMatch ):
	def __init__( self ):
		super( DeathMatch, self ).__init__()
		self.obj_blink = True
		
	def GetPrintName( self ):
		return "KM's Test Scenario"

	def GetGameDescription( self ):
		return "KM Test"

	def GetTeamPlay( self ):
		return Glb.TEAMPLAY_TOGGLE

	def OnLoadGamePlay( self ):
		super( KMTest, self ).OnLoadGamePlay()
		GEUtil.PrecacheSound( "player/ld_chime.wav" )
		GEUtil.PrecacheSound( "player/lld_voodoo.wav" )
		
	def OnPlayerSpawn( self, player ):
		GERules.GetRadar().SetupObjective( player, 0, "", player.GetCleanPlayerName(), Color(120, 120, 0, 255), 0, True )

	def OnPlayerSay( self, player, cmd ):
		assert isinstance( player, GEPlayer.CGEMPPlayer )

		cmd = cmd.lower()
		origin = player.GetAbsOrigin()
		origin[2] += 20.0

		if cmd == "ring":
			GEUtil.CreateTempEnt( TE.RING, origin=origin )
		elif cmd == "beam":
			origin = player.GetEyePosition()
			end = GEUtil.VectorMA( origin, player.GetAimDirection(), 300.0 )
			GEUtil.CreateTempEnt( TE.BEAM, origin=origin, end=end )
		elif cmd == "follow":
			GEUtil.CreateTempEnt( TE.BEAM_FOLLOW, origin=origin, entity=player, duration=3.0 )
		elif cmd == "dust":
			GEUtil.CreateTempEnt( TE.DUST, origin=origin, size=50.0, speed=0.2 )
		elif cmd == "smoke":
			GEUtil.CreateTempEnt( TE.SMOKE, origin=origin, size=50.0, framerate=2 )
		elif cmd == "spark":
			origin = GEUtil.VectorMA( origin, player.GetAimDirection(), 150.0 )
			GEUtil.CreateTempEnt( TE.SPARK, origin=origin )
		elif cmd == "trace":
			origin = player.GetEyePosition()
			end = GEUtil.VectorMA( origin, player.GetAimDirection(), 300.0 )
			hit = GEUtil.Trace( origin, end, TraceOpt.PLAYER, player )
			
			if hit == None:
				GEUtil.HudMessage( None, "No hit!", -1, -1 )
			else:
				player = GEPlayer.ToMPPlayer( hit )
				GEUtil.HudMessage( None, "Hit: " + hit.GetClassname(), -1, -1 )
				GEUtil.HudMessage( None, "Player: " + player.GetPlayerName(), -1, 0.6 )
		elif cmd == "obj":
			self.obj_blink = not self.obj_blink
			for pl in GetPlayers():
				GERules.GetRadar().SetupObjective( pl, 0, "", pl.GetCleanPlayerName(), Color(120, 120, 0, 255), 0, self.obj_blink )
		else:
			return False

		return True
