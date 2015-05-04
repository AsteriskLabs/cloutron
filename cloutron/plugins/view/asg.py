from cloutron.view import *
from cloutron.plugin import *
import boto.ec2.autoscale
from time import localtime, strftime


class AsgView (TerminalView):

	@classmethod
	def configure_subparser(cls, subparsers):
		sp = subparsers.add_parser('autoscale', help='display autoscale group statuses', aliases=('asg','as','a'))
		CloutronView.add_generic_arguments(sp)
		sp.set_defaults(func=AsgView)
		
	def apply_cli_config(self):
		super(AsgView, self).apply_cli_config()
		# if self.args.orientation != None:
		#     self.config.orientation = self.args.orientation

	def sigwinch_handler(self, sig, stack):
		self.render()
		
	def render(self):
		self.info = "Autoscale Groups [%s]" % self.config.region
		self.title = "[Updated " + strftime("%H:%M:%S", localtime()) + "] Cloutron"
		self.do_render("Loading....")
		while True:
			conn = boto.ec2.autoscale.connect_to_region(self.config.region)
			res = conn.get_all_groups()
			output = self.colour("", "white", "grey", [])
			for g in res:
				output = output + "%s (%s/%s/%s)\n" % (g.name, g.min_size, g.max_size, g.desired_capacity)
				res2 = conn.get_all_autoscaling_instances()
				for i in res2:
					if i.group_name == g.name:
						state = ""
						health = ""
						if i.lifecycle_state == "InService":
							state = self.colour("In Service", "green", "grey", [])
						else:
							state = i.lifecycle_state
						if i.health_status == "HEALTHY":
							health = self.colour("Healthy", "green", "grey", [])
						else:
							health = i.health_status
						output = output + " - %s (State: %s Health: %s)\n" % (i.instance_id, state, health)

			self.title = "[Updated " + strftime("%H:%M:%S", localtime()) + "] Cloutron"
			self.do_render(output)
			if float(self.config.poll) < 30:
				time.sleep(30)
			else:
				time.sleep(float(self.config.poll))

class AsgViewPlugin(ViewPlugin):
	plugin_type = 'view'
	name = 'asg'
	view_class = AsgView
